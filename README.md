# AI Code Coach

AI Code Coach answers questions about the code in the `codebase/` folder. It can
**debug** it, **translate** it to another language, or **explain** how it works.

It uses RAG (Retrieval-Augmented Generation): instead of sending your whole
project to the AI, it first searches for the few pieces of code related to your
question and sends only those, together with the question.

## How it works

```
                 (once)  ingest.py
codebase/*.py ──────────────────────────► vector_index/   (searchable "map" of your code)

            (every question)  logic.py
question ──► 1. search vector_index for the 5 most related code chunks   (retriever.py)
         ──► 2. put chunks + question into a prompt                      (prompts.py)
         ──► 3. send the prompt to the Groq LLM, get the answer          (llm.py)
```

| File | What it does |
|------|--------------|
| `config.py` | All settings: folders, API key, model names. |
| `ingest.py` | Reads `codebase/`, splits the code into chunks, turns each chunk into a vector, and saves the index to `vector_index/`. |
| `embeddings.py` | Loads the embedding model (turns text into vectors so you can search by meaning). |
| `retriever.py` | Loads the saved index (or builds it the first time) and finds the chunks related to a question. |
| `prompts.py` | The three prompt templates: Debug, Translate, Explain. |
| `llm.py` | Connects to the Groq language model. |
| `logic.py` | The core: search, then fill the prompt, then ask the LLM. Used by both apps below. |
| `streamlit_app.py` | The web app (chat interface). |
| `app.py` | The same thing as a command-line program. |
| `codebase/` | Put the code you want to ask about here. `buggy_script.py` has a bug on purpose so you can try "Debug Code". |

## Setup

You need Python 3.10 to 3.12 and a free Groq API key.

1. **Get a Groq key** at <https://console.groq.com/keys>. Sign in, click **Create API Key**, and copy it.
2. **Create a `.env` file** next to this README (copy `.env.example`) containing:
   ```
   GROQ_API_KEY=gsk_...your key...
   ```
3. **Install the dependencies** (in a virtual environment):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate        # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Run it

```bash
streamlit run streamlit_app.py     # web app, opens in your browser
python app.py                      # or the command-line version
```

The first run downloads the embedding model (about 90 MB) and builds the index,
so it takes a minute. After that it is fast.

**Changed the files in `codebase/`?** Rebuild the index:
```bash
python ingest.py
```

## Good to know

- Each question is answered on its own. The assistant does not remember earlier messages in the chat.
- To use a different Groq model, set `GROQ_MODEL` in `.env` (the default is `openai/gpt-oss-120b`). If Groq retires a model, pick a new one from <https://console.groq.com/docs/models>.
- You may see a `langchain-community is being sunset` warning. It's only a notice and doesn't affect anything.

## Deployment (Render)

The app runs on Render's free plan as a **Web Service** connected to this GitHub repo.
Every push to `master` redeploys it automatically. Settings used:

| Setting | Value |
|---------|-------|
| Build command | `pip install -r requirements.txt` |
| Start command | `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true` |
| Health check path | `/_stcore/health` |
| Environment variables | `GROQ_API_KEY` (your key), `PYTHON_VERSION=3.12.8` |

The free plan sleeps after 15 minutes without visitors; the next visit takes about a minute to wake it up.

## Built with

- [LangChain](https://python.langchain.com/): glue between the search index, prompts and LLM
- [Streamlit](https://streamlit.io/): the web interface
- [FAISS](https://github.com/facebookresearch/faiss): fast vector search
- [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2): embedding model, run with [FastEmbed](https://github.com/qdrant/fastembed) (light, no PyTorch needed)
- [Groq](https://groq.com/): fast, free-tier LLM API
