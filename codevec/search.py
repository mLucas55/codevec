"""Semantic code search functionality.

Handles searching indexed codebases using natural language queries,
including embedding generation, vector search, and result reranking.
"""

import sys
import logging

# Configure logging before heavy imports
logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger('sentence_transformers').setLevel(logging.WARNING)

import chromadb
from codevec.models import create_embedder, create_reranker

# Load embedding model and reranker
embedder = create_embedder()
reranker = create_reranker()


def generate_query_embedding(query):
    """Convert query text to embedding vector.
    
    Args:
        query: Natural language search query
        
    Returns:
        Embedding vector for the query
    """
    return embedder.embed([query], task_type="query")[0]


def rerank(query, documents, metadatas, distances, n_results):
    """Reorder results using cross-encoder for better relevance.
    
    Args:
        query: Search query string
        documents: List of document strings from initial search
        metadatas: Metadata for each document
        distances: Vector distances from initial search
        n_results: Number of top results to return
        
    Returns:
        List of top n results with rerank scores
    """
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


def get_db_path(root_path):
    """Get the ChromaDB storage path for a given repository.
    
    Args:
        root_path: Root path of the indexed repository
        
    Returns:
        Absolute path to the .codevec directory
    """
    from pathlib import Path
    return str(Path(root_path).resolve() / ".codevec")


def find_repo_root(start_path=None):
    """Walk up directory tree to find a .codevec index, similar to how git finds .git.
    
    Args:
        start_path: Starting directory (default: current working directory)
        
    Returns:
        Path to repository root containing .codevec, or None if not found
    """
    from pathlib import Path
    
    if start_path is None:
        start_path = Path.cwd()
    else:
        start_path = Path(start_path).resolve()
    
    current = start_path
    while current != current.parent:  # Stop at filesystem root
        if (current / ".codevec").is_dir():
            return str(current)
        current = current.parent
    
    # Check root directory too
    if (current / ".codevec").is_dir():
        return str(current)
    
    return None


def search_code(query, root_path=None, n_results=5):
    """Search the indexed codebase for relevant code snippets.
    
    Args:
        query: Search query string
        root_path: Path to indexed repo. If None, auto-detects by walking up from CWD.
        n_results: Number of results to return
    """
    # Auto-detect repo if not provided
    if root_path is None:
        root_path = find_repo_root()
        if root_path is None:
            print("Error: No indexed repository found.")
            print("Either run this command from within an indexed project,")
            print("or specify a path: vec-search 'query' --repo /path/to/project")
            print("\nTo index a project: vec-index /path/to/project")
            sys.exit(1)

    # Connect to ChromaDB in the repository's .codevec directory
    db_path = get_db_path(root_path)
    client = chromadb.PersistentClient(path=db_path, settings=chromadb.Settings(anonymized_telemetry=False))

    try:
        collection = client.get_collection("code_index")
    except Exception as e:
        print(f"Error: Could not load index at {db_path}")
        print("Have you indexed this repository? Run: vec-index /path/to/project")
        sys.exit(1)
    
    query_embedding = generate_query_embedding(query)
    
    # Fetch extra results for reranking (reranker will filter to top n)
    fetch_count = n_results * 2
    raw_results = collection.query(
        query_embeddings=[query_embedding],
        n_results=fetch_count
    )
    
    if not raw_results['documents'][0]:
        print("No results found")
        return

    # Rerank results for better relevance
    results = rerank(
        query,
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