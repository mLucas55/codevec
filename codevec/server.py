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
    texts: List[str]


class RerankRequest(BaseModel):
    query: str
    documents: List[str]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/embed")
def embed_texts(request: TextsRequest):
    """Generate embeddings for a list of texts."""
    if not request.texts:
        return {"embeddings": []}
    
    embeddings = model.encode(request.texts, normalize_embeddings=True)
    return {"embeddings": embeddings.tolist()}


@app.post("/rerank")
def rerank_documents(request: RerankRequest):
    """Rerank documents by relevance to query."""
    if not request.documents:
        return {"rankings": []}
    
    results = reranker.rank(request.query, request.documents, return_documents=False)
    # Convert numpy floats to Python floats for JSON serialization
    rankings = [{"corpus_id": r["corpus_id"], "score": float(r["score"])} for r in results]
    return {"rankings": rankings}