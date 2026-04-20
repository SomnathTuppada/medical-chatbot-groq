from embeddings.embedder import Embedder
from vectorstore.pinecone_client import PineconeClient


class Retriever:
    def __init__(self, top_k: int = 5):
        self.embedder = Embedder()
        self.pinecone = PineconeClient()
        self.top_k = top_k

    def retrieve(self, query: str) -> list[dict]:
        try:
            # 🔥 STEP 1 — Get embedding
            print("🔍 Generating embedding...")
            query_vector = self.embedder.embed_query(query)

            if query_vector is None:
                print("❌ Embedding failed")
                return []

            print("✅ Embedding generated")

            # 🔥 STEP 2 — Query Pinecone
            index = self.pinecone.get_index()

            print("📡 Querying Pinecone...")
            response = index.query(
                vector=query_vector,
                top_k=self.top_k,
                include_metadata=True
            )

            print("✅ Pinecone response received")

            # 🔥 STEP 3 — Parse safely
            matches = response.get("matches", [])

            if not matches:
                print("⚠️ No matches found")
                return []

            results = []
            for match in matches:
                metadata = match.get("metadata", {})

                results.append({
                    "score": match.get("score", 0),
                    "text": metadata.get("text", ""),
                    "source": metadata.get("source", "unknown")
                })

            return results

        except Exception as e:
            print("🔥 RETRIEVER ERROR:", repr(e))
            return []