from google import genai
from google.genai import types
import chromadb

from pathlib import Path
import ast
import sys

from dotenv import load_dotenv
import os

load_dotenv()
GEMENI_KEY = os.getenv("GEMENI_KEY")

gemeni = genai.Client(api_key=GEMENI_KEY)

# Create persistent storage
client = chromadb.PersistentClient(path="./chroma_db")

# Create a collection
try:
    client.delete_collection("code_index")
except:
    pass
collection = client.create_collection(name="code_index")

def generate_embeddings(texts):
    response = gemeni.models.embed_content(
        model="gemini-embedding-001",
        contents=texts,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")
    )

    # Extract the .values from each ContentEmbedding object
    embeddings = [embedding.values for embedding in response.embeddings]
    return embeddings    

def walk_codebase(root_path):
    """Find all Python files in a directory"""
    root = Path(root_path)
    
    # Find all .py files recursively (current folder + all subfolders ----- top down)
    for py_file in root.rglob("*.py"):
        # Skip irrelevant directories 
        if any(segment.startswith('.') or segment == '__pycache__' for segment in py_file.parts):
            continue
        
        # Read file content
        content = py_file.read_text(encoding='utf-8')
        yield (str(py_file), content)  # Returns (file_path, file_content)

def extract_functions_ast(content):
    lines = content.splitlines()
    
    try:
        tree = ast.parse(content)
    except SyntaxError:
        # Handle files with syntax errors
        return []
    
    functions = []  # Typo: you had "function" (singular)
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            start = node.lineno - 1  # AST line numbers are 1-based
            end = node.end_lineno     # This is already inclusive
            
            func_data = "\n".join(lines[start:end])
            
            functions.append({
                "name": node.name,
                "lineno": node.lineno,
                "end_lineno": node.end_lineno,
                "data": func_data,
            })
    
    return functions

def index_codebase(root_path):
    """Index all Python files in the specified directory"""
    print(f"📂 Indexing codebase at: {root_path}")
    
    chunks = []       # The code itself
    metadatas = []    # Info about each chunk
    ids = []
    chunk_id = 0
    
    for file_path, content in walk_codebase(root_path):
        print(f"Found: {file_path}")
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

    print(f"\n🔮 Generating embeddings for {len(chunks)} code chunks...")
    embeddings = generate_embeddings(chunks)

    print("💾 Storing in ChromaDB...")
    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )
    
    print(f"✅ Indexing complete! Indexed {len(chunks)} functions.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python index.py <root_path>")
        print('Example: python index.py ./test-repo')
        sys.exit(1)
    
    root_path = sys.argv[1]
    index_codebase(root_path)