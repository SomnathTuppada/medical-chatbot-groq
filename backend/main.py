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
        retriever = Retriever(top_k=3)
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

    # ⛔ If still loading
    if retriever is None or generator is None:
        return {
            "question": question,
            "answer": "Server is warming up. Please wait a few seconds and retry.",
            "sources": []
        }

    try:
        print("📩 Question:", question)

        contexts = retriever.retrieve(question)
        print("📚 Retrieved:", len(contexts))

        # 🔥 LIMIT CONTEXT COUNT
        contexts = contexts[:2]

        # 🔥 TRIM CONTEXT SIZE (VERY IMPORTANT FOR MEMORY)
        trimmed_contexts = [
            {
                "text": c["text"][:300],
                "source": c["source"],
                "score": c["score"]
            }
            for c in contexts
        ]

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
            "answer": "Server error occurred. Try again.",
            "sources": []
        }