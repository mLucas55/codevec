"""FastAPI server for keeping embedding and reranking models in memory.

Provides REST endpoints for generating embeddings and reranking documents,
improving performance by avoiding model reload on each operation.
"""

from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, CrossEncoder
import uvicorn


app = FastAPI()

print("Initializing embedding model and reranker...")

model = SentenceTransformer("all-MiniLM-L6-v2")
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


class TextsRequest(BaseModel):
    """Request model for embedding generation."""
    texts: List[str]


class RerankRequest(BaseModel):
    """Request model for document reranking."""
    query: str
    documents: List[str]


@app.get("/health")
def health():
    """Health check endpoint.
    
    Returns:
        Status dictionary indicating server health
    """
    return {"status": "ok"}


@app.post("/embed")
def embed_texts(request: TextsRequest):
    """Generate embeddings for a list of texts.
    
    Args:
        request: TextsRequest containing list of strings to embed
        
    Returns:
        Dictionary with 'embeddings' key containing list of embedding vectors
    """
    if not request.texts:
        return {"embeddings": []}
    
    embeddings = model.encode(request.texts, normalize_embeddings=True)
    return {"embeddings": embeddings.tolist()}


@app.post("/rerank")
def rerank_documents(request: RerankRequest):
    """Rerank documents by relevance to query.
    
    Args:
        request: RerankRequest containing query and documents to rank
        
    Returns:
        Dictionary with 'rankings' key containing ranked results with scores
    """
    if not request.documents:
        return {"rankings": []}
    
    results = reranker.rank(request.query, request.documents, return_documents=False)
    # Convert numpy floats to Python floats for JSON serialization
    rankings = [{"corpus_id": r["corpus_id"], "score": float(r["score"])} for r in results]
    return {"rankings": rankings}