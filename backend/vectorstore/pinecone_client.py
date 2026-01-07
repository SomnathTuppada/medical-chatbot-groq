from pinecone import Pinecone, ServerlessSpec
from backend.config import settings


class PineconeClient:
    def __init__(self):
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)

    def create_index_if_not_exists(self, dimension: int):
        existing_indexes = [i["name"] for i in self.pc.list_indexes()]

        if settings.PINECONE_INDEX not in existing_indexes:
            self.pc.create_index(
                name=settings.PINECONE_INDEX,
                dimension=dimension,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region=settings.PINECONE_ENV
                )
            )

    def get_index(self):
        return self.pc.Index(settings.PINECONE_INDEX)

    def upsert_vectors(self, vectors: list[dict], batch_size: int = 100):
        """
        Upserts vectors into Pinecone in batches to avoid payload size limits.
        """
        index = self.get_index()

        total = len(vectors)
        for start in range(0, total, batch_size):
            end = start + batch_size
            batch = vectors[start:end]
            index.upsert(vectors=batch)
