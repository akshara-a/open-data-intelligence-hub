"""Configuration settings for Autonomous Codebase Knowledge Graph Navigator."""

from pathlib import Path
from typing import Literal, Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# Root directory for Task 2
TASK_ROOT_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    model_config = SettingsConfigDict(
        env_file=str(TASK_ROOT_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Neo4j Database Configuration
    NEO4J_URI: str = Field(default="bolt://localhost:7687", description="Neo4j Bolt connection URI")
    NEO4J_USERNAME: str = Field(default="neo4j", description="Neo4j username")
    NEO4J_PASSWORD: str = Field(default="password", description="Neo4j password")
    NEO4J_DATABASE: str = Field(default="neo4j", description="Neo4j database name")

    # Execution Mode
    GRAPH_ENGINE: Literal["mock", "neo4j"] = Field(
        default="mock",
        description="Graph storage engine: 'mock' for in-memory NetworkX or 'neo4j' for live Bolt driver",
    )

    # LLM & Reasoning Configuration
    LLM_PROVIDER: Literal["offline", "openai", "gemini", "groq"] = Field(
        default="offline",
        description="LLM provider: 'offline' for deterministic heuristic synthesis, or API provider",
    )
    OPENAI_API_KEY: Optional[str] = Field(default=None, description="OpenAI API Key")
    GEMINI_API_KEY: Optional[str] = Field(default=None, description="Google Gemini API Key")
    GROQ_API_KEY: Optional[str] = Field(default=None, description="Groq API Key")
    LLM_MODEL: str = Field(default="gpt-4o-mini", description="Model name for generative synthesis")

    # REST API Configuration
    API_HOST: str = Field(default="127.0.0.1", description="FastAPI host")
    API_PORT: int = Field(default=8000, description="FastAPI port")
    DEBUG: bool = Field(default=False, description="Debug mode")

    # Data Seed Paths
    MOCK_SEED_PATH: Path = Field(
        default=TASK_ROOT_DIR / "data" / "mock_graph_seed.json",
        description="Path to mock graph seed JSON",
    )
    CYPHER_SEED_PATH: Path = Field(
        default=TASK_ROOT_DIR / "data" / "sample_architecture_graph.cypher",
        description="Path to sample architecture Cypher seed script",
    )


def get_settings() -> Settings:
    """Retrieve application settings instance."""
    return Settings()
