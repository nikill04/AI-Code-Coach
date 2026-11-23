from functools import cache

from langchain_community.embeddings import FastEmbedEmbeddings

from config import EMBEDDING_MODEL


@cache  # load the model only once, then reuse it (loading takes a few seconds)
def get_embeddings():
    """Return the model that turns text/code into vectors.

    FastEmbed runs the model with ONNX Runtime, which needs far less memory than
    PyTorch, so the app fits on small free servers (like Render's 512 MB plan).
    """
    return FastEmbedEmbeddings(model_name=EMBEDDING_MODEL)
