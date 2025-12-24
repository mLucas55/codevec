import sys
import logging

# Configure logging before heavy imports
logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger('sentence_transformers').setLevel(logging.WARNING)

import chromadb
from codevec.model_loader import ModelLoader

# Load embedding model and optional reranker
model_loader = ModelLoader()
embedder = model_loader.embedder
reranker = model_loader.reranker
reranking_enabled = model_loader.reranking_enabled


def generate_query_embedding(query):
    """Convert query text to embedding vector."""
    return embedder.embed([query], task_type="query")[0]


def rerank(query, documents, metadatas, distances, n_results):
    """Reorder results using cross-encoder for better relevance."""
    ranks = reranker.rank(query, documents, return_documents=False)
    
    results = []
    for r in ranks[:n_results]:
        idx = r['corpus_id']
        results.append({
            'document': documents[idx],
            'metadata': metadatas[idx],
            'distance': distances[idx],
            'rerank_score': r['score']
        })
    return results


def format_results(documents, metadatas, distances, n_results):
    """Format raw vector search results into standard structure."""
    results = []
    for i in range(min(n_results, len(documents))):
        results.append({
            'document': documents[i],
            'metadata': metadatas[i],
            'distance': distances[i],
            'rerank_score': None
        })
    return results


def search_code(query, n_results=5):
    """Search the indexed codebase for relevant code snippets."""

    # Connect to ChromaDB
    client = chromadb.PersistentClient(path="./chroma_db", settings=chromadb.Settings(anonymized_telemetry=False))

    try:
        collection = client.get_collection("code_index")
    except Exception as e:
        logger.error("Could not load index. Have you run index.py first?")
        logger.error(f"Details: {e}")
        sys.exit(1)
        print(f"Searching for: '{query}'")
    
    query_embedding = generate_query_embedding(query)
    
    # Fetch extra results if reranking (reranker will filter to top n)
    fetch_count = n_results * 2 if reranking_enabled else n_results
    raw_results = collection.query(
        query_embeddings=[query_embedding],
        n_results=fetch_count
    )
    
    if not raw_results['documents'][0]:
        print("No results found")
        return

    # Process results
    if reranking_enabled:
        results = rerank(
            query,
            raw_results['documents'][0],
            raw_results['metadatas'][0],
            raw_results['distances'][0],
            n_results
        )
    else:
        results = format_results(
            raw_results['documents'][0],
            raw_results['metadatas'][0],
            raw_results['distances'][0],
            n_results
        )

    # Display results
    print(f"Found {len(results)} results")
    print("\n" + "=" * 80)

    for i, result in enumerate(results, start=1):
        doc = result['document']
        metadata = result['metadata']
        similarity = 1 - result['distance']
        rerank_score = result['rerank_score']

        # Header
        print(f"\n┌─ Result #{i} " + "─" * (68 - len(f"Result #{i}")))

        # Scores
        if rerank_score is not None:
            print(f"│ Similarity: {similarity:.1%}  │  Rerank: {rerank_score:.3f}")
        else:
            print(f"│ Similarity: {similarity:.1%}")
        print("├" + "─" * 79)
        
        # Location
        print(f"│ 📁 File: {metadata['file_path']}")
        print(f"│ ⚙️  Function: {metadata['name']} (line {metadata['line']})")
        print("├" + "─" * 79)
        
        # Code preview (first 20 lines)
        print("│ Code:")
        code_lines = doc.split('\n')
        for j, line in enumerate(code_lines[:20]):
            line_num = metadata['line'] + j
            print(f"│ {line_num:4d} │ {line}")
        if len(code_lines) > 20:
            print("│      │ ...")
        print("└" + "─" * 79)
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python search.py <query>")
        print('Example: python search.py "find email validation"')
        sys.exit(1)
    
    query = " ".join(sys.argv[1:])
    search_code(query)