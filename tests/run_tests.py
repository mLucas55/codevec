"""Automated test runner for semantic search system"""
import re
import chromadb
import logging
from datetime import datetime
from codevec.model_loader import create_embedder
from sentence_transformers import CrossEncoder

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)

# Initialize components
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
embedder = create_embedder()
client = chromadb.PersistentClient(path="./chroma_db", settings=chromadb.Settings(anonymized_telemetry=False))
collection = client.get_collection("code_index")

def generate_query_embedding(query):
    return embedder.embed([query], task_type="query")[0]

def rerank_results(query, documents, metadatas, distances, n_results):
    """Rerank search results using CrossEncoder"""
    ranks = reranker.rank(query, documents, return_documents=False)
    
    reranked = []
    for r in ranks[:n_results]:
        idx = r['corpus_id']
        reranked.append({
            'document': documents[idx],
            'metadata': metadatas[idx],
            'distance': distances[idx],
            'rerank_score': r['score']
        })
    return reranked

def search_code_silent(query, n_results=10):
    """Search without printing output"""
    query_embedding = generate_query_embedding(query)
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results * 2
    )
    
    if not results['documents'][0]:
        return []
    
    reranked = rerank_results(
        query,
        results['documents'][0],
        results['metadatas'][0],
        results['distances'][0],
        n_results
    )
    
    return reranked

def parse_test_queries(file_path):
    """Parse test queries from markdown file"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    test_cases = []
    
    # Pattern to match query entries
    pattern = r'\*\*Query:\*\* "([^"]+)"\s+- \*\*Expected:\*\* `([^`]+)` in ([^\n]+)'
    
    matches = re.findall(pattern, content)
    
    for query, expected_function, file_path in matches:
        test_cases.append({
            'query': query,
            'expected_function': expected_function,
            'expected_file': file_path.strip()
        })
    
    return test_cases

def run_test(test_case, n_results=5):
    """Run a single test and check results"""
    query = test_case['query']
    expected_function = test_case['expected_function']
    expected_file = test_case['expected_file']
    
    results = search_code_silent(query, n_results)
    
    # Check if expected function appears in results
    found_at_rank = None
    
    for rank, result in enumerate(results, 1):
        metadata = result['metadata']
        
        # Check if this result matches expected
        if (metadata['name'] == expected_function and 
            expected_file in metadata['file_path']):
            found_at_rank = rank
            break
    
    return {
        'query': query,
        'expected_function': expected_function,
        'expected_file': expected_file,
        'found_at_rank': found_at_rank,
        'found': found_at_rank is not None,
        'recall_at_1': found_at_rank == 1 if found_at_rank else False,
        'recall_at_3': found_at_rank <= 3 if found_at_rank else False,
        'recall_at_5': found_at_rank <= 5 if found_at_rank else False
    }

def run_all_tests(test_file='test_queries.md'):
    """Run all tests and generate report"""
    print("=" * 80)
    print("SEMANTIC SEARCH SYSTEM - TEST SUITE")
    print("=" * 80)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Parse test cases
    test_cases = parse_test_queries(test_file)
    print(f"Loaded {len(test_cases)} test cases\n")
    
    # Run tests
    results = []
    passed = 0
    
    print("Running tests...")
    print("-" * 80)
    
    for i, test_case in enumerate(test_cases, 1):
        result = run_test(test_case)
        results.append(result)
        
        # Print progress
        status = "✓" if result['found'] else "✗"
        rank_info = f"(rank {result['found_at_rank']})" if result['found'] else "(not found)"
        
        print(f"{status} Test {i:2d}: {result['query'][:50]:50s} {rank_info}")
        
        if result['found']:
            passed += 1
    
    print("-" * 80)
    print()
    
    # Calculate metrics
    total = len(results)
    recall_at_1 = sum(1 for r in results if r['recall_at_1'])
    recall_at_3 = sum(1 for r in results if r['recall_at_3'])
    recall_at_5 = sum(1 for r in results if r['recall_at_5'])
    
    # Print summary
    print("=" * 80)
    print("RESULTS SUMMARY")
    print("=" * 80)
    print(f"Total tests:        {total}")
    print(f"Found in top 5:     {passed} ({passed/total*100:.1f}%)")
    print(f"Not found:          {total - passed}")
    print()
    print("RECALL METRICS")
    print("-" * 80)
    print(f"Recall@1:           {recall_at_1}/{total} ({recall_at_1/total*100:.1f}%)")
    print(f"Recall@3:           {recall_at_3}/{total} ({recall_at_3/total*100:.1f}%)")
    print(f"Recall@5:           {recall_at_5}/{total} ({recall_at_5/total*100:.1f}%)")
    print("=" * 80)
    
    # Calculate average rank for found items
    ranks = [r['found_at_rank'] for r in results if r['found_at_rank']]
    if ranks:
        avg_rank = sum(ranks) / len(ranks)
        print(f"\nAverage rank (when found): {avg_rank:.2f}")
    
    # Show failed tests
    failed = [r for r in results if not r['found']]
    if failed:
        print(f"\n\nFAILED TESTS ({len(failed)}):")
        print("-" * 80)
        for r in failed:
            print(f"  • {r['query']}")
            print(f"    Expected: {r['expected_function']} in {r['expected_file']}")
    
    # Save detailed results to file
    save_results(results)
    
    print(f"\nDetailed results saved to: test_results.txt")
    print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    return results

def save_results(results):
    """Save detailed results to file"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    with open('test_results.txt', 'w') as f:
        f.write("SEMANTIC SEARCH TEST RESULTS\n")
        f.write("=" * 80 + "\n")
        f.write(f"Timestamp: {timestamp}\n\n")
        
        for i, r in enumerate(results, 1):
            f.write(f"Test {i}: {r['query']}\n")
            f.write(f"  Expected: {r['expected_function']} in {r['expected_file']}\n")
            f.write(f"  Found: {'Yes' if r['found'] else 'No'}\n")
            if r['found']:
                f.write(f"  Rank: {r['found_at_rank']}\n")
            f.write(f"  Recall@1: {r['recall_at_1']}\n")
            f.write(f"  Recall@3: {r['recall_at_3']}\n")
            f.write(f"  Recall@5: {r['recall_at_5']}\n")
            f.write("\n")
        
        # Summary statistics
        total = len(results)
        found = sum(1 for r in results if r['found'])
        r1 = sum(1 for r in results if r['recall_at_1'])
        r3 = sum(1 for r in results if r['recall_at_3'])
        r5 = sum(1 for r in results if r['recall_at_5'])
        
        f.write("=" * 80 + "\n")
        f.write("SUMMARY\n")
        f.write("=" * 80 + "\n")
        f.write(f"Total tests: {total}\n")
        f.write(f"Found: {found} ({found/total*100:.1f}%)\n")
        f.write(f"Recall@1: {r1} ({r1/total*100:.1f}%)\n")
        f.write(f"Recall@3: {r3} ({r3/total*100:.1f}%)\n")
        f.write(f"Recall@5: {r5} ({r5/total*100:.1f}%)\n")

if __name__ == "__main__":
    try:
        run_all_tests()
    except Exception as e:
        logger.error(f"Error running tests: {e}")
        import traceback
        traceback.print_exc()
