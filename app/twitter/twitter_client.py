from app.schema.outage_schema import TwitterConfig
from typing import List, Dict
from fastapi import HTTPException
import tweepy
import logging
from app.twitter.outage_extractor import OutageExtractor
from app.schema.outage_schema import Outage


logger = logging.getLogger(__name__)


class TwitterClient:
    def __init__(self, config: TwitterConfig):
        self.client = tweepy.Client(
            bearer_token=config.bearer_token,
            consumer_key=config.consumer_key,
            consumer_secret=config.consumer_secret,
            access_token=config.access_token,
            access_token_secret=config.access_token_secret,
            wait_on_rate_limit=True,
        )
        self.extractor = OutageExtractor()

    def fetch_reg_tweets(self, max_results: int = 10) -> List[Dict]:
        """Fetch recent tweets from REG account"""
        try:
            # Replace with actual REG Twitter username
            reg_username = "reg_rwanda"

            user = self.client.get_user(username=reg_username)
            if not user.data:
                raise HTTPException(
                    status_code=404, detail="REG Twitter account not found"
                )

            tweets = self.client.get_users_tweets(
                id=user.data.id,
                max_results=max_results,
                tweet_fields=["created_at", "public_metrics", "text"],
            )

            if not tweets.data:
                return []

            return [
                {
                    "id": tweet.id,
                    "text": tweet.text,
                    "created_at": tweet.created_at,
                    "metrics": tweet.public_metrics,
                }
                for tweet in tweets.data
            ]

        except Exception as e:
            logger.error(f"Error fetching tweets: {e}")
            return []

    def process_tweets(self, tweets: List[Dict]) -> List[Outage]:
        """Process tweets and extract outage information"""
        outages = []

        for tweet in tweets:
            outage = self.extractor.process_tweet(tweet["text"], str(tweet["id"]))
            if outage:
                outage.timestamp = tweet["created_at"]
                outages.append(outage)

        return outages
