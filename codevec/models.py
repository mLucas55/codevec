from sentence_transformers import SentenceTransformer, CrossEncoder
import requests

class LocalEmbedder:
    """Embedding model using local sentence-transformers."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
    
    def embed(self, texts: list[str], task_type: str = "document") -> list[list[float]]:
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()

class RemoteEmbedder:
    """Interface to generate embeddings on FastAPI server"""

    def __init__(self, url: str = "http://localhost:8000"):
        self.url = url
    
    def embed(self, texts: list[str], task_type: str = "document") -> list[list[float]]:
        response = requests.post(f"{self.url}/embed", json={"texts": texts})
        return response.json()["embeddings"]

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
        response = requests.post(f"{self.url}/rerank", json={"query": query, "documents": documents})
        return response.json()["rankings"]


def is_server_running(url="http://localhost:8000"):
    try:
        return requests.get(f"{url}/health", timeout=1).ok
    except:
        return False

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