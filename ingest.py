"""Build the search index for the files in codebase/.

Run this again whenever you add or change files in codebase/:
    python ingest.py
"""
import os

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter

from config import CODEBASE_DIR, INDEX_DIR
from embeddings import get_embeddings


def build_index():
    # 1. Load every .py file in codebase/ as a "document".
    loader = DirectoryLoader(
        CODEBASE_DIR,
        glob="**/*.py",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        exclude=["**/venv/**", "**/__pycache__/**", "**/.git/**"],
    )
    documents = loader.load()

    # Store paths like "buggy_script.py" instead of the full path on this computer.
    for doc in documents:
        doc.metadata["source"] = os.path.relpath(doc.metadata["source"], CODEBASE_DIR)

    # 2. Split the files into smaller chunks. The Python splitter prefers to cut
    #    at class/function boundaries, so chunks stay readable.
    splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON, chunk_size=1000, chunk_overlap=200
    )
    chunks = splitter.split_documents(documents)
    if not chunks:
        raise RuntimeError(f"No Python code found in {CODEBASE_DIR}. Add some .py files first.")

    # 3. Turn each chunk into a vector and save the index to disk.
    vectorstore = FAISS.from_documents(chunks, get_embeddings())
    vectorstore.save_local(INDEX_DIR)

    print(f"Indexed {len(chunks)} code chunks from {len(documents)} files.")
    return vectorstore


if __name__ == "__main__":
    build_index()
