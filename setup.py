from setuptools import setup, find_packages

setup(
    name='codevec',
    version='0.10',
    author="Lucas Monroe",
    author_email="lucas.i.monroe1@gmail.com",
    packages=find_packages(),
    install_requires=[
        'chromadb',
        'sentence-transformers',
        'fastapi',
        'uvicorn'
    ],
    entry_points={
        "console_scripts": [
            "vec = codevec:help",
            "vec-index = codevec:indexer",
            "vec-search = codevec:searcher",
            "vec-server = codevec.server:run_server",
        ]
    }
)