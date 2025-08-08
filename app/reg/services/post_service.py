from sqlalchemy.orm import Session
from app.db.models.post import Post
from typing import List, Optional, Dict
from datetime import datetime, timedelta, timezone


class PostService:
    def __init__(self, db: Session):
        self.db = db

    def create_post(self, post_data: Dict) -> Post:
        """Create a new post record"""
        post = Post(**post_data)
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return post

    def get_post_by_id(self, post_id: str) -> Optional[Post]:
        """Get post by Post ID"""
        return self.db.query(Post).filter(Post.tweet_id == post_id).first()

    def get_unprocessed_posts(self, limit: int = 100) -> List[Post]:
        """Get posts that haven't been processed yet."""
        return self.db.query(Post).filter(Post.processed == False).limit(limit).all()

    def mark_post_as_processed(self, post_id: str, error: str = None) -> Optional[Post]:
        """Mark a post as processed."""
        post = self.db.query(Post).filter(Post.tweet_id == post_id).first()
        if post:
            post.processed = True
            if error:
                post.processing_error = error
            self.db.commit()
            self.db.refresh(post)
        return post

    def get_recent_posts(self, hours: int = 24) -> List[Post]:
        """Get recent posts."""
        cutoff_time = datetime.now(timezone.now()) - timedelta(hours=hours)
        return (
            self.db.query(Post)
            .filter(Post.tweet_created_at >= cutoff_time)
            .order_by(Post.tweet_created_at.desc())
            .all()
        )

    def bulk_create_posts(self, posts_data: List[Dict]) -> List[Post]:
        """Create multiple posts at once."""
        tweets = []
        for tweet_data in posts_data:
            # Skip if tweet already exists
            existing = self.get_post_by_id(tweet_data["tweet_id"])
            if not existing:
                tweet = Post(**tweet_data)
                tweets.append(tweet)

        if tweets:
            self.db.add_all(tweets)
            self.db.commit()
            for tweet in tweets:
                self.db.refresh(tweet)

        return tweets
