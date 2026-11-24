"""Backend API of AI Code Coach (runs on Render):  uvicorn api:app --reload

The web page in frontend/ (hosted on Vercel) sends each question here and shows the answer.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from logic import process_query
from prompts import PROMPTS

app = FastAPI(title="AI Code Coach API")

# The web page lives on a different website (Vercel), so the browser needs
# permission ("CORS") to call this API from there.
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


class Question(BaseModel):
    task: str       # "Debug Code", "Translate Code" or "Explain Algorithm"
    question: str


@app.get("/")
def health():
    """Render calls this to check the server is up."""
    return {"status": "ok", "tasks": list(PROMPTS)}


@app.post("/ask")
def ask(body: Question):
    if body.task not in PROMPTS:
        raise HTTPException(status_code=400, detail=f"Unknown task. Choose one of: {list(PROMPTS)}")
    answer, docs = process_query(body.task, body.question)
    sources = [{"source": doc.metadata["source"], "code": doc.page_content} for doc in docs]
    return {"answer": answer, "sources": sources}
