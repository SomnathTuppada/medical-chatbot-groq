import requests
from config import settings

class Embedder:
    def __init__(self):
        self.api_url = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
        self.headers = {
            "Authorization": f"Bearer {settings.HF_TOKEN}"
        }

    def embed_query(self, query):
        try:
            print("🌍 Calling HF URL:", self.api_url)

            response = requests.post(
                url=self.api_url,   # 🔥 explicit
                headers=self.headers,
                json={"inputs": query},
                timeout=10
            )

            print("📡 Status Code:", response.status_code)
            print("🔍 HF RAW:", response.text[:200])

            if response.status_code != 200:
                return None

            data = response.json()

            if isinstance(data, list):
                return data[0]

            return data

        except Exception as e:
            print("🔥 EMBEDDING ERROR:", e)
            return None