from sentence_transformers import SentenceTransformer, CrossEncoder
import requests

class LocalEmbedder:
    """Embedding model using local sentence-transformers."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
    
    def embed(self, texts: list[str], task_type: str = "document") -> list[list[float]]:
        embeddings = self.model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
        return embeddings.tolist()

class RemoteEmbedder:
    """Interface to generate embeddings on FastAPI server"""

    def __init__(self, url: str = "http://localhost:8000"):
        self.url = url
    
    def embed(self, texts: list[str], task_type: str = "document") -> list[list[float]]:
        try:
            response = requests.post(f"{self.url}/embed", json={"texts": texts}, timeout=60)
            response.raise_for_status()
            return response.json()["embeddings"]
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to connect to embedding server at {self.url}: {e}") from e

class LocalReranker:
    """Cross-encoder reranker for improving search result relevance."""
    
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model = CrossEncoder(model_name)
    
    def rank(self, query: str, documents: list[str], return_documents: bool = False):
        return self.model.rank(query, documents, return_documents=return_documents)


class RemoteReranker:
    """Interface to rerank documents on FastAPI server."""
    
    def __init__(self, url: str = "http://localhost:8000"):
        self.url = url
    
    def rank(self, query: str, documents: list[str], return_documents: bool = False):
        try:
            response = requests.post(f"{self.url}/rerank", json={"query": query, "documents": documents}, timeout=60)
            response.raise_for_status()
            return response.json()["rankings"]
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to connect to reranker server at {self.url}: {e}") from e


# Cache server status to avoid multiple health checks
_server_status = None

def is_server_running(url="http://localhost:8000"):
    global _server_status
    if _server_status is None:
        try:
            _server_status = requests.get(f"{url}/health", timeout=1).ok
        except requests.RequestException:
            _server_status = False
    return _server_status


def create_embedder():
    """Create an embedder (remote if server running, else local)."""
    if is_server_running():
        return RemoteEmbedder()
    else:
        return LocalEmbedder()


def create_reranker():
    """Create a reranker (remote if server running, else local)."""
    if is_server_running():
        return RemoteReranker()
    else:
        return LocalReranker()