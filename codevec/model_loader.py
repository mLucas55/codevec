from sentence_transformers import CrossEncoder

from codevec.config import get_model_type, get_api_key, get_reranking
from codevec.embeddings import Embedder, GeminiEmbedder, LocalEmbedder


def create_embedder() -> Embedder:
    """Create an embedder based on the configured model type."""
    model_type = get_model_type()
    if model_type == "local":
        return LocalEmbedder()
    elif model_type == "gemini":
        return GeminiEmbedder(api_key=get_api_key())
    else:
        raise ValueError(f"Unknown model type: {model_type}")


class ModelLoader:
    def __init__(self):
        self.embedder = self._load_embedder()
        self.reranking_enabled = get_reranking()
        self.reranker = self._load_reranker() if self.reranking_enabled else None

    def _load_embedder(self) -> Embedder:
        return create_embedder()

    def _load_reranker(self) -> CrossEncoder:
        return CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')