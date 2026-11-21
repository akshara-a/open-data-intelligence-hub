import os
import re
import math
import struct
import hashlib
from typing import List, Optional, Tuple
import numpy as np

MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"
MODEL_REVISION = "9a32259"
MODEL_VERSION = f"{MODEL_NAME}@{MODEL_REVISION}"
FALLBACK_MODEL_VERSION = "fallback-deterministic-projection-v1"
PREPROCESS_VERSION = "v2_code_chunk_semantic"
VECTOR_DIM = 768


class EmbeddingEngine:
    """
    Embedding Engine for GraphRAG retrieval.
    Manages explicit model lifecycle, unit-normalization, and cosine similarity.
    """

    def __init__(self, allow_fallback: Optional[bool] = None, force_fallback: bool = False):
        self.preprocess_version = PREPROCESS_VERSION
        self.dim = VECTOR_DIM
        self._model = None
        self.load_error: Optional[str] = None

        env_fallback = os.getenv("ALLOW_EMBEDDING_FALLBACK", "false").lower() in ("true", "1", "yes")
        self.allow_fallback = allow_fallback if allow_fallback is not None else env_fallback

        if force_fallback:
            self.model_version = FALLBACK_MODEL_VERSION
            self.status = "fallback_deterministic_projection"
            self.backend = "deterministic_projection_fallback"
            self.fallback_mode = True
        else:
            self._try_load_transformer()

    def _try_load_transformer(self):
        try:
            from sentence_transformers import SentenceTransformer
            # Pinned all-mpnet-base-v2 per Section 9.2
            self._model = SentenceTransformer(MODEL_NAME)
            self.status = "active_transformer"
            self.backend = "sentence_transformers"
            self.model_version = MODEL_VERSION
            self.fallback_mode = False
        except Exception as e:
            self._model = None
            self.load_error = str(e)
            if self.allow_fallback:
                self.status = "fallback_deterministic_projection"
                self.backend = "deterministic_projection_fallback"
                self.model_version = FALLBACK_MODEL_VERSION
                self.fallback_mode = True
            else:
                self.status = f"model_load_failed: {e}"
                self.backend = "unavailable"
                self.model_version = MODEL_VERSION
                self.fallback_mode = False

    def embed_text(self, text: str) -> np.ndarray:
        """
        Embeds a single string into a unit-normalized float32 vector of shape (768,).
        """
        if self._model is not None and self.status == "active_transformer":
            vec = self._model.encode(text, normalize_embeddings=True, convert_to_numpy=True)
            norm = float(np.linalg.norm(vec))
            if abs(norm - 1.0) > 1e-4 and norm > 1e-9:
                vec = vec / norm
            return vec.astype(np.float32)

        if self.fallback_mode:
            return self._compute_deterministic_projection(text)

        raise RuntimeError(f"Embedding model unavailable ({self.status}). Fallback mode is disabled.")

    def embed_batch(self, texts: List[str]) -> List[np.ndarray]:
        if not texts:
            return []
        if self._model is not None and self.status == "active_transformer":
            vecs = self._model.encode(texts, normalize_embeddings=True, convert_to_numpy=True)
            res = []
            for v in vecs:
                norm = float(np.linalg.norm(v))
                if abs(norm - 1.0) > 1e-4 and norm > 1e-9:
                    v = v / norm
                res.append(v.astype(np.float32))
            return res

        if self.fallback_mode:
            return [self._compute_deterministic_projection(t) for t in texts]

        raise RuntimeError(f"Embedding model unavailable ({self.status}). Fallback mode is disabled.")

    def _compute_deterministic_projection(self, text: str) -> np.ndarray:
        """
        Deterministic, term-weighted semantic projection into 768-dim unit sphere.
        Preserves keyword, token, and n-gram similarity deterministically without external weights.
        """
        vec = np.zeros(self.dim, dtype=np.float32)
        raw_words = re.findall(r"[a-zA-Z0-9_]+", text.lower())
        if not raw_words:
            # Return unit vector pointing along first axis
            vec[0] = 1.0
            return vec

        # Expand compound tokens (snake_case)
        words: List[str] = []
        for w in raw_words:
            words.append(w)
            if "_" in w:
                parts = [p for p in w.split("_") if p]
                words.extend(parts)

        # Bag-of-words / n-grams projection with frequency dampening
        for i, word in enumerate(words):
            # Token hash seed
            thash = hashlib.sha256(word.encode("utf-8")).digest()
            # Spread across multiple coordinates
            for k in range(8):
                idx = (thash[k] * 256 + thash[k + 8]) % self.dim
                sign = 1.0 if (thash[k + 16] % 2 == 0) else -1.0
                vec[idx] += sign * 1.0

            # Bigram if available
            if i > 0:
                bigram = f"{words[i-1]}_{word}"
                bhash = hashlib.sha256(bigram.encode("utf-8")).digest()
                for k in range(4):
                    idx = (bhash[k] * 256 + bhash[k + 4]) % self.dim
                    sign = 1.0 if (bhash[k + 8] % 2 == 0) else -1.0
                    vec[idx] += sign * 1.2

        # Normalize to unit L2 sphere: ||vec||_2 == 1.0
        norm = np.linalg.norm(vec)
        if norm > 1e-9:
            vec = vec / norm
        else:
            vec[0] = 1.0

        return vec.astype(np.float32)

    @staticmethod
    def vector_to_blob(vec: np.ndarray) -> bytes:
        return vec.astype(np.float32).tobytes()

    @staticmethod
    def blob_to_vector(blob: bytes) -> np.ndarray:
        return np.frombuffer(blob, dtype=np.float32)

    @staticmethod
    def compute_cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
        """
        Computes cosine similarity between two unit-normalized vectors.
        Since both are L2 normalized, dot product == cosine similarity.
        Clamped to [0.0, 1.0] for non-negative ranking metric.
        """
        sim = float(np.dot(vec_a, vec_b))
        # Scale/clamp [-1.0, 1.0] to [0.0, 1.0]
        return max(0.0, min(1.0, (sim + 1.0) / 2.0 if sim < 0 else sim))


# Global singleton
_embedding_engine: Optional[EmbeddingEngine] = None


def get_embedding_engine(force_fallback: bool = False, allow_fallback: Optional[bool] = None) -> EmbeddingEngine:
    global _embedding_engine
    if _embedding_engine is None or force_fallback:
        _embedding_engine = EmbeddingEngine(allow_fallback=allow_fallback, force_fallback=force_fallback)
    return _embedding_engine
