from sqlalchemy import Column, String, DateTime, Boolean, Text, Integer
from sqlalchemy.dialects.postgresql import JSONB
from app.db.models.base_model import BaseModel


class Post(BaseModel):
    __tablename__ = "posts"

    # Twitter data
    tweet_id = Column(String, unique=True, index=True, nullable=False)
    text = Column(Text, nullable=False)
    author_id = Column(String, index=True)

    # Tweet metadata
    is_mention = Column(Boolean, default=False)
    is_reply = Column(Boolean, default=False)
    in_reply_to_tweet_id = Column(String)

    # Timestamps
    tweet_created_at = Column(DateTime(timezone=True))
    fetched_at = Column(DateTime(timezone=True))

    # Engagement metrics
    retweet_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    reply_count = Column(Integer, default=0)
    quote_count = Column(Integer, default=0)

    # Processing status
    processed = Column(Boolean, default=False)
    processing_error = Column(Text)

    # Store raw tweet data
    raw_data = Column(JSONB)

    def __repr__(self):
        return f"<Tweet(id={self.tweet_id}, processed={self.processed})>"
