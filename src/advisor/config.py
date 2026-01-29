"""Project configuration and constants."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ModelConfig:
    verifier_model: str = "gpt-5-nano"
    advisor_model: str = "gpt-5-mini"
    embedding_model: str = "text-embedding-3-small"


@dataclass(frozen=True)
class VectorstoreConfig:
    chunk_size: int = 1000
    chunk_overlap: int = 200
    k_results: int = 5


MODEL_CONFIG = ModelConfig()
VECTORSTORE_CONFIG = VectorstoreConfig()


def project_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def docs_dir() -> Path:
    return project_root() / "docs"


def index_dir() -> Path:
    return project_root() / "data"


def index_path() -> Path:
    return index_dir() / "faiss_index"
