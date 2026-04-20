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
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json={"inputs": query},
                timeout=10
            )

            print("🔍 HF RAW:", response.text[:200])

            if response.status_code != 200:
                print("❌ HF ERROR:", response.status_code)
                return None

            if not response.text:
                print("❌ Empty HF response")
                return None

            data = response.json()

            # 🔥 HF returns nested list sometimes
            if isinstance(data, list):
                return data[0]

            return data

        except Exception as e:
            print("🔥 EMBEDDING ERROR:", e)
            return None