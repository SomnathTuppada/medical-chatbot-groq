import os
from dotenv import load_dotenv
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parent / ".env"

# 🔥 THIS IS THE FIX
load_dotenv(dotenv_path=ENV_PATH, override=True)

class Settings:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_ENV = os.getenv("PINECONE_ENV")
    PINECONE_INDEX = os.getenv("PINECONE_INDEX")
    HF_TOKEN = os.getenv("HF_TOKEN")


settings = Settings()