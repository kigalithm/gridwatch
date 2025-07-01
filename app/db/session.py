import asyncio, os
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from app.core.settings import Settings
from sentence_transformers import SentenceTransformer
from sqlalchemy.pool import QueuePool

settings = Settings()


engine = create_engine(
    url=settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,  # number of connections to keep in the pool
    max_overflow=20,  # additional connections beyond pool_size
    pool_timeout=30,  # seconds to wait before giving up on getting a connection
    pool_recycle=1800,  # recycle connections every 30 mins
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


executor = ThreadPoolExecutor()

# Load the pre-cached model
model_path = "/app/cached_model"
if os.path.exists(model_path):
    # Use the cached model from Docker layer
    embedding_model = SentenceTransformer(model_path)
else:
    # Fallback for local development
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


# Dependency
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_embedding(text: str) -> list[float]:
    loop = asyncio.get_event_loop()
    embedding = await loop.run_in_executor(executor, embedding_model.encode, text)
    return embedding.tolist()


def get_sync_embedding(text: str) -> list[float]:
    return asyncio.run(get_embedding(text))
