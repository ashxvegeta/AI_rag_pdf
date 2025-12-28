from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag.rag_engine import RAGEngine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend
    allow_methods=["*"],
    allow_headers=["*"],
)

# initialize RAG engine
rag = RAGEngine("sample.pdf")

class QueryRequest(BaseModel):
    query: str

@app.get("/health")
def health():
    return {"status": "RAG is running healthy"}

@app.post("/ask")
def ask_question(request: QueryRequest):
    question = request.query.strip()   # ✅ FIXED

    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        answer = rag.ask(question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
