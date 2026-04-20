import requests
from config import settings

class Embedder:
    def __init__(self):
        self.api_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"
        self.headers = {
            "Authorization": f"Bearer {settings.HF_TOKEN}"
        }

    def embed_texts(self, texts):
        embeddings = []
        for text in texts:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json={"inputs": text}
            )
            embeddings.append(response.json()[0])
        return embeddings

    def embed_query(self, query):
        response = requests.post(
            self.api_url,
            headers=self.headers,
            json={"inputs": query}
        )
        return response.json()[0]