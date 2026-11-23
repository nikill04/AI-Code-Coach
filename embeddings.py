from functools import cache

from langchain_huggingface import HuggingFaceEmbeddings

from config import EMBEDDING_MODEL


@cache  # load the model only once, then reuse it (loading takes a few seconds)
def get_embeddings():
    """Return the model that turns text/code into vectors."""
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
