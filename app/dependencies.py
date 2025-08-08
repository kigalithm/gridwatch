import asyncio, os
from concurrent.futures import ThreadPoolExecutor
from sentence_transformers import SentenceTransformer
from app.reg.twitter.twitter_client import TwitterClient
from app.reg.schema.outage_schema import (
    TwitterConfig,
)
from app.core.config import Settings

settings = Settings()

executor = ThreadPoolExecutor()


twitter_config = TwitterConfig(
    bearer_token=settings.BEARER_TOKEN,
    consumer_key=settings.CONSUMER_KEY,
    consumer_secret=settings.CONSUMER_SECRET,
    access_token=settings.ACCESS_TOKEN,
    access_token_secret=settings.ACCESS_TOKEN_SECRET,
)

twitter_client = TwitterClient(config=twitter_config)


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
