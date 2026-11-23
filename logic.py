"""The core RAG (Retrieval-Augmented Generation) step, shared by the web app and CLI.

RAG in three steps:
  1. Retrieve: find the code chunks most related to the question.
  2. Augment:  paste those chunks into a prompt together with the question.
  3. Generate: send the prompt to the LLM and return its answer.
"""
from langchain_core.output_parsers import StrOutputParser

from llm import get_llm
from prompts import PROMPTS
from retriever import get_retriever


def process_query(task, query):
    """Answer `query` for the given task ("Debug Code", "Translate Code" or "Explain Algorithm").

    Returns (answer_text, list_of_code_chunks_used).
    """
    # 1. Retrieve
    docs = get_retriever().invoke(query)

    # 2. Augment: label each chunk with the file it came from.
    context = "\n\n".join(
        f"--- File: {doc.metadata['source']} ---\n{doc.page_content}" for doc in docs
    )

    # 3. Generate: prompt -> LLM -> plain text.
    chain = PROMPTS[task] | get_llm() | StrOutputParser()
    answer = chain.invoke({"context": context, "query": query})

    return answer, docs
