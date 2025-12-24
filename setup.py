from setuptools import setup, find_packages

setup(
    name='codevec',
    version='0.3',
    author="Lucas Monroe",
    author_email="lucas.i.monroe1@gmail.com",
    packages=find_packages(),
    install_requires=[
        'chromadb',
        'sentence-transformers',
        'google-genai',
    ],
    entry_points={
        "console_scripts": [
            "vec = codevec:help",
            "vec-index = codevec:indexer",
            "vec-search = codevec:searcher",
            "vec-config = codevec:configurator",
        ]
    }
)