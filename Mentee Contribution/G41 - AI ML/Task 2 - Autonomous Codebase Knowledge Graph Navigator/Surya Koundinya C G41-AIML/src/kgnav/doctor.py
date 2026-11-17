"""`kgnav doctor`: verify the Gemini key, that configured model IDs exist for THIS key, and Neo4j connectivity."""
from __future__ import annotations

import os

import httpx

from .config import load_config

_URL = "https://generativelanguage.googleapis.com/v1beta/models"


def _list_models(key: str) -> set[str]:
    names: set[str] = set()
    token = None
    while True:
        params = {"pageSize": 1000, **({"pageToken": token} if token else {})}
        r = httpx.get(_URL, headers={"x-goog-api-key": key}, params=params, timeout=30)
        r.raise_for_status()
        body = r.json()
        for m in body.get("models", []):
            if "generateContent" in m.get("supportedGenerationMethods", []):
                names.add(m["name"].removeprefix("models/"))
        token = body.get("nextPageToken")
        if not token:
            return names


def run() -> int:
    cfg = load_config()
    ok = True
    key = os.getenv("GEMINI_API_KEY", "")
    if not key:
        print("FAIL  GEMINI_API_KEY not set (create one at https://aistudio.google.com/apikey)")
        ok = False
    else:
        try:
            names = _list_models(key)
            print(f"OK    Gemini key valid; {len(names)} generateContent models visible")
            for label, model in (("investigation", cfg.model), ("report", cfg.model_synth)):
                if model in names:
                    print(f"OK    {label} model '{model}' is available")
                else:
                    ok = False
                    close = sorted(n for n in names if "flash" in n and "image" not in n and "tts" not in n and "live" not in n)
                    print(f"FAIL  {label} model '{model}' not available. Flash models for your key: {', '.join(close[:15])}")
        except Exception as e:  # noqa: BLE001
            ok = False
            print(f"FAIL  Gemini model listing failed: {e}")
    try:
        from .neo4j_client import GraphClient

        GraphClient(cfg).query("RETURN 1 AS ok")
        print(f"OK    Neo4j reachable at {cfg.neo4j_uri}")
    except Exception as e:  # noqa: BLE001
        ok = False
        print(f"FAIL  Neo4j: {e}")
    print("Check your live free-tier limits (RPM / requests per day) at https://aistudio.google.com/rate-limit")
    return 0 if ok else 1
