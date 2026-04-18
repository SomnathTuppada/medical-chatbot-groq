from embeddings.embedder import Embedder
from vectorstore.pinecone_client import PineconeClient


class Retriever:
    def __init__(self, top_k: int = 5):
        self.embedder = Embedder()
        self.pinecone = PineconeClient()
        self.top_k = top_k

    def retrieve(self, query: str) -> list[dict]:
        query_vector = self.embedder.embed_query(query)
        index = self.pinecone.get_index()

        response = index.query(
            vector=query_vector,
            top_k=self.top_k,
            include_metadata=True
        )

        results = []
        for match in response["matches"]:
            results.append({
                "score": match["score"],
                "text": match["metadata"]["text"],
                "source": match["metadata"]["source"]
            })

        return results
