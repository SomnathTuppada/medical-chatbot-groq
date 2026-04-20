from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from ingestion.pdf_loader import load_all_pdfs
from ingestion.text_splitter import split_text
from embeddings.embedder import Embedder
from vectorstore.pinecone_client import PineconeClient
from rag.retriever import Retriever
from rag.generator import Generator

app = FastAPI(title="Medical RAG Chatbot")

# 🌐 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 GLOBALS (start empty)
embedder = None
retriever = None
generator = None


# 🚀 LOAD ON STARTUP (IMPORTANT FIX)
@app.on_event("startup")
def load_models():
    global embedder, retriever, generator

    print("🚀 Loading models...")

    try:
        embedder = Embedder()
        retriever = Retriever(top_k=2)
        generator = Generator()

        print("✅ Models loaded successfully")

    except Exception as e:
        print("🔥 Startup error:", e)


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
    global retriever, generator

    try:
        print("📩 Question:", question)

        # STEP 1
        print("➡️ Calling retriever...")
        contexts = retriever.retrieve(question)

        if not contexts:
            return {
                "question": question,
                "answer": "No relevant information found or system is warming up.",
                "sources": []
            }

        print("📚 Retrieved:", len(contexts))

        contexts = contexts[:2]

        # STEP 2
        print("➡️ Calling generator...")
        answer = generator.generate_answer(question, contexts)
        print("✅ Generator done")

        return {
            "question": question,
            "answer": answer,
            "sources": [
                {"source": c["source"], "score": c["score"]}
                for c in contexts
            ]
        }

    except Exception as e:
        print("🔥 FULL ERROR:", repr(e))
        return {
            "question": question,
            "answer": "Server error occurred.",
            "sources": []
        }