import os
from functools import cache

from langchain_community.vectorstores import FAISS

from config import INDEX_DIR, NUM_CHUNKS
from embeddings import get_embeddings
from ingest import build_index


@cache  # build/load the index only once, then reuse it
def get_retriever():
    """Return an object that finds the code chunks most related to a question."""
    if os.path.exists(os.path.join(INDEX_DIR, "index.faiss")):
        # allow_dangerous_deserialization: the index is a file we created
        # ourselves with ingest.py, so it is safe to load.
        vectorstore = FAISS.load_local(
            INDEX_DIR, get_embeddings(), allow_dangerous_deserialization=True
        )
    else:
        # First run (or index deleted): build it now.
        vectorstore = build_index()
    return vectorstore.as_retriever(search_kwargs={"k": NUM_CHUNKS})
