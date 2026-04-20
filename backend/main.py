from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from ingestion.pdf_loader import load_all_pdfs
from ingestion.text_splitter import split_text
from embeddings.embedder import Embedder
from vectorstore.pinecone_client import PineconeClient
from rag.retriever import Retriever
from rag.generator import Generator

# Initialize once 
embedder = Embedder()
retriever = Retriever(top_k=3)
generator = Generator()

app = FastAPI(title="Medical RAG Chatbot")

# CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "Medical RAG backend running"}

@app.get("/debug/check-path")
def debug_check_path():
    folder = Path("data/medical_pdfs")
    return {
        "exists": folder.exists(),
        "absolute_path": str(folder.resolve()),
        "files_found": [f.name for f in folder.glob("*")]
    }

@app.get("/query")
def query_medical_bot(question: str):
    try:
        print("📩 Question:", question)

        contexts = retriever.retrieve(question)
        print("📚 Retrieved:", len(contexts))

        # 🔥 REDUCE LOAD (CRITICAL)
        contexts = contexts[:2]

        # 🔥 Trim context text (VERY IMPORTANT)
        trimmed_contexts = []
        for c in contexts:
            trimmed_contexts.append({
                "text": c["text"][:300],   # limit size
                "source": c["source"],
                "score": c["score"]
            })

        answer = generator.generate_answer(question, trimmed_contexts)

        print("✅ Answer generated")

        return {
            "question": question,
            "answer": answer,
            "sources": [
                {"source": c["source"], "score": c["score"]}
                for c in trimmed_contexts
            ]
        }

    except Exception as e:
        print("🔥 ERROR:", e)

        return {
            "question": question,
            "answer": "Server is warming up. Please try again.",
            "sources": []
        }