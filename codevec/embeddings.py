from abc import ABC, abstractmethod

from google import genai
from google.genai import types
from sentence_transformers import SentenceTransformer

class Embedder(ABC):
    @abstractmethod
    def embed(self, texts: list[str], task_type: str = "document") -> list[list[float]]:
        pass

class LocalEmbedder(Embedder):
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the local embedder using sentence-transformers.
        
        Args:
            model_name: The sentence-transformers model to use. 
                       Default is 'all-MiniLM-L6-v2' which is a fast and lightweight model.
        """
        self.model = SentenceTransformer(model_name)
    
    def embed(self, texts: list[str], task_type: str = "document") -> list[list[float]]:
        """
        Generate embeddings for the given texts using the local model.
        
        Args:
            texts: List of text strings to embed
            task_type: Not used by local embedder (for API compatibility only)
            
        Returns:
            List of embedding vectors (each vector is a list of floats)
        """
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()


class GeminiEmbedder(Embedder):
    def __init__(self, api_key: str, model_name: str = "gemini-embedding-001"):
        """
        Initialize Gemini client using a Google Gemini model.
        
        Args:
            api_key: Google Gemini API key
            model_name: The Gemini embedding model to use. 
                       Default is 'gemini-embedding-001' which is a free and lightweight model.
        """
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
    
    def embed(self, texts: list[str], task_type: str = "document") -> list[list[float]]:
        """
        Generate embeddings for the given texts using the Gemini API.
        
        Args:
            texts: List of text strings to embed
            task_type: Either "document" (for indexing) or "query" (for search queries)
            
        Returns:
            List of embedding vectors (each vector is a list of floats)
        """
        # Map task_type to Gemini's task type constants
        gemini_task_type = "RETRIEVAL_DOCUMENT" if task_type == "document" else "CODE_RETRIEVAL_QUERY"
        
        response = self.client.models.embed_content(
            model=self.model_name,
            contents=texts,
            config=types.EmbedContentConfig(task_type=gemini_task_type)
        )
        
        # Extract the .values from each ContentEmbedding object
        embeddings = [embedding.values for embedding in response.embeddings]
        return embeddings
