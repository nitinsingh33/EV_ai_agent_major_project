from qdrant_client import QdrantClient
from qdrant_client.http import models as qdrant_models
from core.config import config
from rag.embeddings import embed_texts
import os


COLLECTION_NAME = config.QDRANT_COLLECTION
VECTOR_SIZE = 384
DISTANCE = qdrant_models.Distance.COSINE

client = QdrantClient(
    url=config.QDRANT_URL,
    api_key=config.QDRANT_API_KEY,
)

def ensure_collection():
    if COLLECTION_NAME not in [c.name for c in client.get_collections().collections]:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=qdrant_models.VectorParams(
                size=VECTOR_SIZE,
                distance=DISTANCE
            )
        )

ensure_collection()

def upsert(chunks: list[dict]):
    """
    chunks: List of dicts with keys 'text' and optional 'metadata'
    """
    texts = [chunk['text'] for chunk in chunks]
    embeddings = embed_texts(texts)
    points = []
    for i, chunk in enumerate(chunks):
        points.append(
            qdrant_models.PointStruct(
                id=None,
                vector=embeddings[i],
                payload={
                    "text": chunk["text"],
                    "metadata": chunk.get("metadata", {})
                }
            )
        )
    client.upsert(collection_name=COLLECTION_NAME, points=points)

def search(query: str, top_k: int = 5, filters: dict = None):
    embedding = embed_texts([query])[0]
    filter_obj = None
    if filters:
        filter_obj = qdrant_models.Filter(
            must=[
                qdrant_models.FieldCondition(
                    key=k,
                    match=qdrant_models.MatchValue(value=v)
                ) for k, v in filters.items()
            ]
        )
    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=embedding,
        limit=top_k,
        filter=filter_obj
    )
    hits = []
    for r in results:
        payload = r.payload or {}
        hits.append({
            "text": payload.get("text"),
            "score": r.score,
            "metadata": payload.get("metadata", {})
        })
    return hits