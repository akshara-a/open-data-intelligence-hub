"""Runtime configuration (env vars / .env)."""
from __future__ import annotations

import os
from dataclasses import dataclass

try:  # optional, so pure-logic modules/tests work without the dependency
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # pragma: no cover
    pass


@dataclass(frozen=True)
class Config:
    neo4j_uri: str
    neo4j_user: str
    neo4j_password: str
    neo4j_database: str
    provider: str
    model: str          # investigation (tool-use loop) model
    model_synth: str    # report-writing model
    synth_max_tokens: int
    synth_fallbacks: tuple  # models tried in order if the report model is overloaded/out of quota
    max_rows: int
    query_timeout_s: float
    max_steps: int
    max_grounding_retries: int


def load_config() -> Config:
    g = os.getenv
    investigate = g("KGNAV_MODEL_INVESTIGATE") or g("KGNAV_MODEL") or "gemini-3.5-flash-lite"
    fb = g("KGNAV_SYNTH_FALLBACKS")
    fallbacks = tuple(x.strip() for x in fb.split(",") if x.strip()) if fb is not None else (investigate,)
    return Config(
        neo4j_uri=g("NEO4J_URI", "bolt://localhost:7687"),
        neo4j_user=g("NEO4J_USER", "neo4j"),
        neo4j_password=g("NEO4J_PASSWORD", "kgnav-password"),
        neo4j_database=g("NEO4J_DATABASE", "neo4j"),
        provider=g("KGNAV_PROVIDER", "gemini"),
        # KGNAV_MODEL (if set) applies to both phases unless a phase-specific variable overrides it.
        # Free-tier quotas are per model: a Flash-Lite model has a far larger daily request allowance, so it
        # drives the many-call investigation loop, while the stronger Flash model writes the report.
        model=investigate,
        model_synth=g("KGNAV_MODEL_SYNTH") or g("KGNAV_MODEL") or "gemini-3.8-flash",
        synth_max_tokens=int(g("KGNAV_SYNTH_MAX_TOKENS", "16000")),
        synth_fallbacks=fallbacks,
        max_rows=int(g("KGNAV_MAX_ROWS", "500")),
        query_timeout_s=float(g("KGNAV_QUERY_TIMEOUT_S", "20")),
        max_steps=int(g("KGNAV_MAX_STEPS", "12")),
        max_grounding_retries=int(g("KGNAV_GROUNDING_RETRIES", "2")),
    )
