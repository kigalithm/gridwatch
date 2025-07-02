from concurrent.futures import ThreadPoolExecutor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from app.core.settings import Settings
from sqlalchemy.pool import QueuePool

settings = Settings()


engine = create_engine(
    url=settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


executor = ThreadPoolExecutor()

# Load the pre-cached model
# model_path = "/app/cached_model"
# if os.path.exists(model_path):
#     # Use the cached model from Docker layer
#     embedding_model = SentenceTransformer(model_path)
# else:
#     # Fallback for local development
#     embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


# Dependency
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
