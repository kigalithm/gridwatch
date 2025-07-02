import asyncio, os
from concurrent.futures import ThreadPoolExecutor
from sentence_transformers import SentenceTransformer

executor = ThreadPoolExecutor()


# Load the pre-cached model
model_path = "/app/cached_model"
if os.path.exists(model_path):
    # Use the cached model from Docker layer
    embedding_model = SentenceTransformer(model_path)
else:
    # Fallback for local development
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


async def get_embedding(text: str) -> list[float]:
    loop = asyncio.get_event_loop()
    embedding = await loop.run_in_executor(executor, embedding_model.encode, text)
    return embedding.tolist()


def get_sync_embedding(text: str) -> list[float]:
    return asyncio.run(get_embedding(text))
