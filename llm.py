from langchain_groq import ChatGroq

from config import GROQ_API_KEY, GROQ_MODEL


def get_llm():
    """Return the Groq chat model used to answer questions."""
    if not GROQ_API_KEY:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Put it in a .env file "
            "(see .env.example) or set it as an environment variable."
        )
    return ChatGroq(model=GROQ_MODEL, api_key=GROQ_API_KEY, temperature=0)
