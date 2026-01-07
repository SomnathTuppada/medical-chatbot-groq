from fastapi import FastAPI
from backend.ingestion.pdf_loader import load_all_pdfs
from backend.ingestion.pdf_loader import load_all_pdfs
from backend.ingestion.text_splitter import split_text
from backend.ingestion.pdf_loader import load_all_pdfs
from backend.ingestion.text_splitter import split_text
from backend.embeddings.embedder import Embedder
from backend.vectorstore.pinecone_client import PineconeClient
from backend.embeddings.embedder import Embedder
from backend.ingestion.pdf_loader import load_all_pdfs
from backend.ingestion.text_splitter import split_text
from backend.rag.retriever import Retriever
from backend.rag.retriever import Retriever
from backend.rag.generator import Generator
from fastapi.middleware.cors import CORSMiddleware




app = FastAPI(title="Medical RAG Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "Medical RAG backend running"}


@app.get("/debug/load-pdfs")
def debug_load_pdfs():
    data = load_all_pdfs("data/medical_pdfs")
    return {
        "pdf_count": len(data),
        "files": list(data.keys()),
        "sample_text_preview": {
            k: v[:500] for k, v in data.items()
        }
    }

from pathlib import Path

@app.get("/debug/check-path")
def debug_check_path():
    folder = Path("data/medical_pdfs")
    return {
        "exists": folder.exists(),
        "absolute_path": str(folder.resolve()),
        "files_found": [f.name for f in folder.glob("*")]
    }

@app.get("/debug/chunk-pdfs")
def debug_chunk_pdfs():
    pdfs = load_all_pdfs("data/medical_pdfs")

    result = {}
    for name, text in pdfs.items():
        chunks = split_text(text)
        result[name] = {
            "total_chunks": len(chunks),
            "sample_chunk": chunks[0][:500]
        }

    return result

@app.get("/debug/embed-sample")
def debug_embed_sample():
    pdfs = load_all_pdfs("data/medical_pdfs")
    text = list(pdfs.values())[0]
    chunks = split_text(text)

    embedder = Embedder()
    vectors = embedder.embed_texts(chunks[:3])

    return {
        "chunks_used": 3,
        "vector_dimension": len(vectors[0]),
        "sample_vector_preview": vectors[0][:8]
    }

@app.get("/debug/create-index")
def debug_create_index():
    embedder = Embedder()
    pinecone_client = PineconeClient()

    pinecone_client.create_index_if_not_exists(dimension=384)

    return {"status": "Index ready"}

@app.post("/debug/ingest")
def debug_ingest():
    pdfs = load_all_pdfs("data/medical_pdfs")
    embedder = Embedder()
    pinecone_client = PineconeClient()

    vectors = []
    vector_id = 0

    for filename, text in pdfs.items():
        chunks = split_text(text)
        embeddings = embedder.embed_texts(chunks)

        for chunk, embedding in zip(chunks, embeddings):
            vectors.append({
                "id": f"chunk-{vector_id}",
                "values": embedding,
                "metadata": {
                    "text": chunk,
                    "source": filename
                }
            })
            vector_id += 1

    pinecone_client.upsert_vectors(vectors)

    return {"vectors_uploaded": len(vectors)}

@app.get("/debug/env-check")
def debug_env_check():
    from backend.config import settings
    return {
        "pinecone_api_key_set": bool(settings.PINECONE_API_KEY),
        "pinecone_env": settings.PINECONE_ENV,
        "pinecone_index": settings.PINECONE_INDEX
    }

@app.get("/debug/retrieve")
def debug_retrieve(query: str):
    retriever = Retriever(top_k=5)
    results = retriever.retrieve(query)
    return {
        "query": query,
        "results": results
    }

@app.get("/query")
def query_medical_bot(question: str):
    retriever = Retriever(top_k=5)
    generator = Generator()

    contexts = retriever.retrieve(question)
    answer = generator.generate_answer(question, contexts)

    return {
        "question": question,
        "answer": answer,
        "sources": [
            {"source": c["source"], "score": c["score"]}
            for c in contexts
        ]
    }
0


















