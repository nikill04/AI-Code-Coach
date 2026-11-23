"""All project settings in one place."""
import os

from dotenv import load_dotenv

# Read the .env file (if there is one) so GROQ_API_KEY becomes available.
load_dotenv()

# Folders
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CODEBASE_DIR = os.path.join(BASE_DIR, "codebase")      # code the assistant can "read"
INDEX_DIR = os.path.join(BASE_DIR, "vector_index")     # where the search index is saved

# Language model (Groq)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

# Embedding model: turns code into vectors so we can search it by meaning.
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# How many code chunks to send to the LLM with each question.
NUM_CHUNKS = 5
