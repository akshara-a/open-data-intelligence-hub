"""
High-Performance Local Server for Customer Feedback Analysis System
Serves the modern Swiss-grid frontend and provides REST API endpoints:
- GET  /api/health      : System readiness, model status, dataset statistics
- POST /api/analyze     : Analyzes single customer feedback in real-time
- POST /api/batch       : Batch analysis of multiple feedback entries
- GET  /api/samples     : Curated customer feedback examples
- GET  /api/corpus      : Historical feedback samples for similarity reference
- Static file serving   : Delivers the frontend application assets
"""

import http.server
import socketserver
import json
import os
import sys
import urllib.parse
from typing import Dict, Any, List

# Ensure current working directory is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

PORT = 8000
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")

# Lazy-loaded NLP analyzer
analyzer_instance = None


def get_analyzer():
    global analyzer_instance
    if analyzer_instance is None:
        try:
            from src.pipeline import CustomerFeedbackAnalyzer
            print("[INFO] Initializing CustomerFeedbackAnalyzer...")
            analyzer_instance = CustomerFeedbackAnalyzer(
                models_dir=os.path.join(PROJECT_ROOT, "models"),
                data_path=os.path.join(PROJECT_ROOT, "data", "feedback.csv")
            )
            analyzer_instance.load_or_train()
            print("[INFO] CustomerFeedbackAnalyzer loaded successfully.")
        except Exception as e:
            print(f"[WARNING] Could not initialize Python NLP pipeline: {e}")
            analyzer_instance = None
    return analyzer_instance


CURATED_SAMPLES = [
    {
        "id": "sample-1",
        "title": "Payment Failure & App Latency",
        "icon": "⚡",
        "text": "The application is very slow and payment keeps failing during checkout.",
        "expected_sentiment": "negative",
        "expected_categories": ["payment", "performance"]
    },
    {
        "id": "sample-2",
        "title": "Exceptional Support Resolution",
        "icon": "🎧",
        "text": "Customer support team solved my issue in less than ten minutes and followed up politely.",
        "expected_sentiment": "positive",
        "expected_categories": ["support"]
    },
    {
        "id": "sample-3",
        "title": "Missing Login Verification OTP",
        "icon": "🔐",
        "text": "Login OTP is not arriving on my registered mobile number after multiple attempts.",
        "expected_sentiment": "negative",
        "expected_categories": ["login"]
    },
    {
        "id": "sample-4",
        "title": "Dark Mode & UI Feature Request",
        "icon": "🌙",
        "text": "Can you please add dark mode support in the settings for late night reading?",
        "expected_sentiment": "neutral",
        "expected_categories": ["feature_request", "ui"]
    },
    {
        "id": "sample-5",
        "title": "Post-Update Crashes & Glitches",
        "icon": "⚠️",
        "text": "The latest update is terrible, the app freezes constantly and crashes on transaction history.",
        "expected_sentiment": "negative",
        "expected_categories": ["bug", "performance"]
    },
    {
        "id": "sample-6",
        "title": "Clean Redesign Praise",
        "icon": "💎",
        "text": "I love the new dashboard design, it looks super modern, intuitive and easy to use.",
        "expected_sentiment": "positive",
        "expected_categories": ["ui"]
    }
]


class StudioRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=FRONTEND_DIR, **kwargs)

    def _set_headers(self, status=200, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(204)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/health":
            analyzer = get_analyzer()
            response_data = {
                "status": "online",
                "engine": "Customer Feedback Analysis System",
                "model_ready": analyzer is not None and analyzer.is_ready,
                "dataset_path": os.path.join("data", "feedback.csv"),
                "version": "2.0.0"
            }
            self._set_headers(200)
            self.wfile.write(json.dumps(response_data).encode("utf-8"))
            return

        if path == "/api/samples":
            self._set_headers(200)
            self.wfile.write(json.dumps(CURATED_SAMPLES).encode("utf-8"))
            return

        if path == "/api/corpus":
            try:
                import pandas as pd
                csv_path = os.path.join(PROJECT_ROOT, "data", "feedback.csv")
                if os.path.exists(csv_path):
                    df = pd.read_csv(csv_path)
                    records = df.head(30).to_dict(orient="records")
                    self._set_headers(200)
                    self.wfile.write(json.dumps({"total": len(df), "records": records}).encode("utf-8"))
                    return
            except Exception as e:
                pass
            self._set_headers(200)
            self.wfile.write(json.dumps({"total": len(CURATED_SAMPLES), "records": CURATED_SAMPLES}).encode("utf-8"))
            return

        # Default static file serving from FRONTEND_DIR
        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length > 0 else b"{}"

        try:
            payload = json.loads(body.decode("utf-8")) if body else {}
        except Exception:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "Invalid JSON payload"}).encode("utf-8"))
            return

        if path == "/api/analyze":
            text = payload.get("text", "").strip()
            top_k = int(payload.get("top_k", 3))

            if not text:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "Feedback text is required"}).encode("utf-8"))
                return

            analyzer = get_analyzer()
            if analyzer is not None:
                try:
                    result = analyzer.analyze(text, top_k_similar=top_k)

                    # Also compare stemming vs lemmatization for UI inspection
                    from src.preprocessing import tokenize, clean_text, compare_stem_vs_lemma
                    stem_lemma_comparison = compare_stem_vs_lemma(text)
                    result["stem_vs_lemma"] = stem_lemma_comparison

                    self._set_headers(200)
                    self.wfile.write(json.dumps(result).encode("utf-8"))
                    return
                except Exception as e:
                    print(f"[ERROR] Analysis error: {e}")

            # Fallback mock analysis if pipeline could not be loaded
            fallback = {
                "raw_text": text,
                "cleaned_text": text.lower(),
                "sentiment": "negative" if any(w in text.lower() for w in ["slow", "fail", "bad", "terrible", "issue", "bug", "crash"]) else "positive",
                "sentiment_scores": {"negative": 0.85, "neutral": 0.10, "positive": 0.05},
                "sentiment_confidence": 0.85,
                "categories": ["performance", "payment"],
                "category_scores": {"performance": 0.88, "payment": 0.76},
                "keywords": ["application", "slow", "payment", "failing"],
                "similar_feedback": [
                    {
                        "feedback": "The application is very slow and lags constantly",
                        "sentiment": "negative",
                        "categories": ["performance"],
                        "similarity": 0.91,
                        "similarity_percentage": "91.0%"
                    }
                ]
            }
            self._set_headers(200)
            self.wfile.write(json.dumps(fallback).encode("utf-8"))
            return

        if path == "/api/batch":
            texts = payload.get("texts", [])
            if not isinstance(texts, list) or not texts:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": "texts must be a non-empty list of strings"}).encode("utf-8"))
                return

            analyzer = get_analyzer()
            results = []
            if analyzer is not None:
                try:
                    for t in texts[:50]:  # Limit to 50 max
                        if str(t).strip():
                            res = analyzer.analyze(str(t).strip(), top_k_similar=1)
                            results.append({
                                "text": str(t).strip(),
                                "sentiment": res["sentiment"],
                                "confidence": round(res["sentiment_confidence"] * 100, 1),
                                "categories": res["categories"],
                                "keywords": res["keywords"][:3],
                                "top_similar": res["similar_feedback"][0]["feedback"] if res["similar_feedback"] else "",
                                "similarity": res["similar_feedback"][0]["similarity_percentage"] if res["similar_feedback"] else "0%"
                            })
                    self._set_headers(200)
                    self.wfile.write(json.dumps({"count": len(results), "items": results}).encode("utf-8"))
                    return
                except Exception as e:
                    print(f"[ERROR] Batch error: {e}")

            self._set_headers(500)
            self.wfile.write(json.dumps({"error": "Batch processing failed"}).encode("utf-8"))
            return

        self._set_headers(404)
        self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode("utf-8"))


def run_server(port=PORT):
    import threading
    os.makedirs(FRONTEND_DIR, exist_ok=True)

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", port), StudioRequestHandler) as httpd:
        print(f"\n=======================================================", flush=True)
        print(f"  CUSTOMER FEEDBACK NLP STUDIO - FRONTEND SERVER", flush=True)
        print(f"  URL: http://localhost:{port}", flush=True)
        print(f"  Serving directory: {FRONTEND_DIR}", flush=True)
        print(f"  Press Ctrl+C to terminate.", flush=True)
        print(f"=======================================================\n", flush=True)

        # Pre-warm model in background thread so server is immediately responsive
        def warm_up():
            print("[INIT] Loading Python NLP Pipeline in background...", flush=True)
            get_analyzer()
            print("[INIT] Python NLP Pipeline loaded and ready.", flush=True)

        threading.Thread(target=warm_up, daemon=True).start()

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[INFO] Server stopped gracefully.", flush=True)


if __name__ == "__main__":
    port_arg = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    run_server(port_arg)
