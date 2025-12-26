"""Model interfaces for embeddings and reranking.

Provides both local (in-process) and remote (server-based) implementations
for generating embeddings and reranking search results.
"""

from sentence_transformers import SentenceTransformer, CrossEncoder
import requests

class LocalEmbedder:
    """Embedding model using local sentence-transformers.
    
    Runs the embedding model in-process without requiring a server.
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize the local embedding model.
        
        Args:
            model_name: HuggingFace model identifier (default: "all-MiniLM-L6-v2")
        """
        self.model = SentenceTransformer(model_name)
    
    def embed(self, texts: list[str], task_type: str = "document") -> list[list[float]]:
        """Generate embeddings for text snippets.
        
        Args:
            texts: List of text strings to embed
            task_type: Type of embedding task (unused, for API compatibility)
            
        Returns:
            List of embedding vectors (normalized)
        """
        embeddings = self.model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
        return embeddings.tolist()

class RemoteEmbedder:
    """Interface to generate embeddings via FastAPI server.
    
    Delegates embedding generation to a remote server, which keeps
    models loaded in memory for better performance.
    """

    def __init__(self, url: str = "http://localhost:8000"):
        self.url = url
    
    def embed(self, texts: list[str], task_type: str = "document") -> list[list[float]]:
        """Generate embeddings via remote server.
        
        Args:
            texts: List of text strings to embed
            task_type: Type of embedding task (unused, for API compatibility)
            
        Returns:
            List of embedding vectors
            
        Raises:
            ConnectionError: If server is unreachable or returns an error
        """
        try:
            response = requests.post(f"{self.url}/embed", json={"texts": texts}, timeout=60)
            response.raise_for_status()
            return response.json()["embeddings"]
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to connect to embedding server at {self.url}: {e}") from e

class LocalReranker:
    """Cross-encoder reranker for improving search result relevance.
    
    Uses a cross-encoder model to rerank initial search results based on
    deeper semantic understanding of query-document pairs.
    """
    
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        """Initialize the local reranker.
        
        Args:
            model_name: HuggingFace cross-encoder model identifier
        """
        self.model = CrossEncoder(model_name)
    
    def rank(self, query: str, documents: list[str], return_documents: bool = False):
        """Rank documents by relevance to query.
        
        Args:
            query: Search query string
            documents: List of document strings to rank
            return_documents: Whether to include document text in results
            
        Returns:
            List of ranking results with scores and corpus IDs
        """
        return self.model.rank(query, documents, return_documents=return_documents)


class RemoteReranker:
    """Interface to rerank documents via FastAPI server.
    
    Delegates reranking to a remote server for better performance
    when models are already loaded in memory.
    """
    
    def __init__(self, url: str = "http://localhost:8000"):
        self.url = url
    
    def rank(self, query: str, documents: list[str], return_documents: bool = False):
        """Rank documents by relevance via remote server.
        
        Args:
            query: Search query string
            documents: List of document strings to rank
            return_documents: Whether to include document text (unused)
            
        Returns:
            List of ranking results with scores and corpus IDs
            
        Raises:
            ConnectionError: If server is unreachable or returns an error
        """
        try:
            response = requests.post(f"{self.url}/rerank", json={"query": query, "documents": documents}, timeout=60)
            response.raise_for_status()
            return response.json()["rankings"]
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to connect to reranker server at {self.url}: {e}") from e


# Cache server status to avoid multiple health checks
_server_status = None

def is_server_running(url="http://localhost:8000"):
    """Check if the embedding server is running and healthy.
    
    Caches the result to avoid repeated health checks.
    
    Args:
        url: Base URL of the server to check
        
    Returns:
        True if server is running and responsive, False otherwise
    """
    global _server_status
    if _server_status is None:
        try:
            _server_status = requests.get(f"{url}/health", timeout=1).ok
        except requests.RequestException:
            _server_status = False
    return _server_status


def create_embedder():
    """Create an embedder instance (remote if server running, else local).
    
    Automatically detects if an embedding server is available and uses it
    for better performance, otherwise falls back to local processing.
    
    Returns:
        RemoteEmbedder if server is available, otherwise LocalEmbedder
    """
    if is_server_running():
        return RemoteEmbedder()
    else:
        return LocalEmbedder()


def create_reranker():
    """Create a reranker instance (remote if server running, else local).
    
    Automatically detects if a reranking server is available and uses it
    for better performance, otherwise falls back to local processing.
    
    Returns:
        RemoteReranker if server is available, otherwise LocalReranker
    """
    if is_server_running():
        return RemoteReranker()
    else:
        return LocalReranker()