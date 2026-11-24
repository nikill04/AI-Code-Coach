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
| `logic.py` | The core: search, then fill the prompt, then ask the LLM. Used by the API and the CLI below. |
| `api.py` | The backend: a small web API (FastAPI) with one endpoint, `POST /ask`, that runs `logic.py`. |
| `frontend/index.html` | The website (chat interface). A single HTML page that sends questions to `api.py`. |
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
python app.py                      # command-line version

uvicorn api:app --reload           # or the backend API, on http://127.0.0.1:8000
```

To use the website against your local API, change `API_URL` at the top of the
`<script>` in `frontend/index.html` to `http://127.0.0.1:8000` and open the file in
your browser. You can also try the API itself at <http://127.0.0.1:8000/docs>.

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

## Deployment

The app is in two parts:

```
browser ──► website (Vercel)  ──POST /ask──►  API (Render)  ──►  Groq LLM
            frontend/index.html               api.py
```

**Website: Vercel**, <https://ai-code-coach-vercel-url>. Vercel project `ai-code-coach`,
root directory `frontend/`. It is a plain HTML file, so there is no build step.

**API: Render**, <https://ai-code-coach-kghe.onrender.com>. A free **Web Service**
connected to this GitHub repo; every push to `master` redeploys it. Settings used:

| Setting | Value |
|---------|-------|
| Build command | `pip install -r requirements.txt` |
| Start command | `uvicorn api:app --host 0.0.0.0 --port $PORT` |
| Health check path | `/` |
| Environment variables | `GROQ_API_KEY` (your key), `PYTHON_VERSION=3.12.8` |

The free Render plan sleeps after 15 minutes without visitors, so the first
question after a quiet spell takes about a minute while it wakes up.

## Built with

- [LangChain](https://python.langchain.com/): glue between the search index, prompts and LLM
- [FastAPI](https://fastapi.tiangolo.com/): the backend API
- [Vercel](https://vercel.com/) (website) and [Render](https://render.com/) (API): hosting
- [FAISS](https://github.com/facebookresearch/faiss): fast vector search
- [all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2): embedding model, run with [FastEmbed](https://github.com/qdrant/fastembed) (light, no PyTorch needed)
- [Groq](https://groq.com/): fast, free-tier LLM API
