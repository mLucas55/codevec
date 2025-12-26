"""Code indexing functionality for CodeVec.

Handles parsing Python files, extracting functions using AST,
generating embeddings, and storing them in a ChromaDB collection.
"""

import logging
from pathlib import Path
import ast

# Configure logging first, before heavy imports
logging.basicConfig(
    level=logging.WARNING,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

import chromadb
from codevec.models import create_embedder


embedder = create_embedder()


def generate_embeddings(texts):
    """Generate vector embeddings for code snippets.
    
    Args:
        texts: List of code strings to embed
        
    Returns:
        List of embedding vectors
    """
    return embedder.embed(texts)

def walk_codebase(root_path):
    """Find all Python files in a directory.
    
    Recursively walks the directory tree, skipping hidden directories,
    __pycache__, and other irrelevant paths.
    
    Args:
        root_path: Root directory to scan
        
    Yields:
        Tuple of (file_path, file_content) for each Python file
    """
    root = Path(root_path)
    
    for py_file in root.rglob("*.py"):
        # Skip irrelevant directories 
        if any(segment.startswith('.') or segment == '__pycache__' for segment in py_file.parts):
            continue
        
        # Read file content
        content = py_file.read_text(encoding='utf-8')
        yield (str(py_file), content)  # Returns (file_path, file_content)

def extract_functions_ast(content):
    """Extract function definitions from Python code using AST parsing.
    
    Args:
        content: Python source code as a string
        
    Returns:
        List of dicts containing function metadata:
        - name: Function name
        - lineno: Starting line number
        - end_lineno: Ending line number
        - data: Full function source code
    """
    lines = content.splitlines()
    
    try:
        tree = ast.parse(content)
    except SyntaxError:
        # Handle files with syntax errors
        return []
    
    functions = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            start = node.lineno - 1  # AST line numbers are 1-based
            end = node.end_lineno 
            
            func_data = "\n".join(lines[start:end])
            
            functions.append({
                "name": node.name,
                "lineno": node.lineno,
                "end_lineno": node.end_lineno,
                "data": func_data,
            })
    
    return functions

def get_db_path(root_path):
    """Get the ChromaDB storage path for a given repository.
    
    Args:
        root_path: Root path of the indexed repository
        
    Returns:
        Absolute path to the .codevec directory
    """
    return str(Path(root_path).resolve() / ".codevec")


def add_to_gitignore(root_path):
    """Add .codevec to .gitignore if not already present.
    
    Creates .gitignore if it doesn't exist, or appends to existing file.
    Prevents the index directory from being committed to version control.
    
    Args:
        root_path: Root path of the repository
    """
    gitignore_path = Path(root_path).resolve() / ".gitignore"
    
    # Check if .codevec is already ignored
    if gitignore_path.exists():
        content = gitignore_path.read_text()
        if ".codevec" in content.splitlines():
            return  # Already ignored
        # Append to existing file
        with open(gitignore_path, "a") as f:
            if not content.endswith("\n"):
                f.write("\n")
            f.write(".codevec\n")
    else:
        # Create new .gitignore
        gitignore_path.write_text(".codevec\n")
    
    print("Added .codevec to .gitignore")


def index_codebase(root_path):
    """Index all Python files in the specified directory.
    
    Walks the directory tree, extracts functions from Python files,
    generates embeddings, and stores them in a ChromaDB collection
    at .codevec/. Creates or replaces existing index.
    
    Args:
        root_path: Root directory of the codebase to index
    """
    print(f"Indexing codebase: {root_path}")
    
    # Add .codevec to .gitignore
    add_to_gitignore(root_path)
    
    # Create persistent storage inside the indexed repository
    db_path = get_db_path(root_path)
    client = chromadb.PersistentClient(path=db_path, settings=chromadb.Settings(anonymized_telemetry=False))

    # Create a fresh collection (delete existing one if present)
    try:
        client.delete_collection("code_index")
    except Exception:
        pass  # Collection doesn't exist yet
    collection = client.create_collection(name="code_index")
    
    chunks = []
    metadatas = []
    ids = []
    chunk_id = 0
    
    print("Scanning Python files...")
    
    for file_path, content in walk_codebase(root_path):
        functions = extract_functions_ast(content)
        
        for func in functions:
            chunks.append(func["data"])

            metadatas.append({
                "file_path": file_path,
                "name": func["name"],
                "line": func["lineno"],
                "type": "function"
            })

            ids.append(f"chunk_{chunk_id}")
            chunk_id += 1

    print(f"Generating embeddings for {len(chunks)} code chunks...")
    embeddings = generate_embeddings(chunks)

    print("Storing embeddings in database...")
    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )
    
    print(f"Indexing complete. {len(chunks)} functions indexed.")