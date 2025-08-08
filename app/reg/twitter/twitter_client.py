from app.reg.schema.outage_schema import TwitterConfig
from typing import List, Dict
from fastapi import HTTPException
import tweepy
import logging
from app.reg.twitter.outage_extractor import OutageExtractor
from app.reg.schema.outage_schema import Outage
from app.core.config import Settings
import json, os
from datetime import datetime
from typing import Optional


logger = logging.getLogger(__name__)
settings = Settings()


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
        """Fetch recent tweets from REG, including replies and expanded user tweets."""
        try:
            reg_username = "reg_rwanda"

            # Get REG user ID
            user = self.client.get_user(username=reg_username)
            if not user.data:
                raise HTTPException(
                    status_code=404, detail="REG Twitter account not found"
                )

            # Fetch tweets (including replies) + expand referenced tweets
            last_id = self._get_last_processed_id("last_fetched_id.txt")
            response = self.client.get_users_tweets(
                id=user.data.id,
                max_results=max_results,
                since_id=last_id,
                tweet_fields=[
                    "created_at",
                    "public_metrics",
                    "text",
                    "in_reply_to_user_id",
                    "in_reply_to_status_id",
                ],
                expansions=["referenced_tweets.id"],
            )

            tweets = response.data or []
            if tweets:
                self._set_last_processed_id("last_fetched_id.txt", tweets[0].id)
                referenced = {t.id: t for t in (response.includes.get("tweets") or [])}

                formatted = []
                for tweet in tweets:
                    original_tweet = referenced.get(tweet.in_reply_to_status_id)
                    formatted.append(
                        {
                            "id": tweet.id,
                            "text": tweet.text,
                            "created_at": (
                                tweet.created_at.isoformat()
                                if tweet.created_at
                                else None
                            ),
                            "is_reply": tweet.in_reply_to_status_id is not None,
                            "in_reply_to_status_id": tweet.in_reply_to_status_id,
                            "original_user_text": (
                                original_tweet.text if original_tweet else None
                            ),
                            "metrics": {
                                "retweet_count": tweet.public_metrics.get(
                                    "retweet_count", 0
                                ),
                                "like_count": tweet.public_metrics.get("like_count", 0),
                                "reply_count": tweet.public_metrics.get(
                                    "reply_count", 0
                                ),
                                "quote_count": tweet.public_metrics.get(
                                    "quote_count", 0
                                ),
                            },
                            "fetched_at": datetime.now().isoformat(),
                        }
                    )
                self._save_tweets_to_json(formatted, reg_username)
                return formatted

        except Exception as e:
            logger.error(f"Error fetching tweets: {e}")
            return []

    def fetch_mentions(self, max_results: int = 10) -> List[Dict]:
        """Fetch recent tweets that mention @reg_rwanda (from any user)."""
        try:
            reg_user = self.client.get_user(username="reg_rwanda")
            if not reg_user.data:
                raise HTTPException(
                    status_code=404,
                    detail="REG Twitter account not found",
                )
            last_id = self._get_last_processed_id("last_mention_id.txt")
            # Fetch recent mentions
            response = self.client.get_users_mentions(
                id=reg_user.data.id,
                max_results=max_results,
                since_id=last_id,
                tweet_fields=["created_at", "public_metrics", "text", "author_id"],
            )

            tweets = response.data or []

            if tweets:
                self._set_last_processed_id("last_mention_id.txt", tweets[0].id)

                formatted = []
                for tweet in tweets:
                    formatted.append(
                        {
                            "id": tweet.id,
                            "text": tweet.text,
                            "created_at": (
                                tweet.created_at.isoformat()
                                if tweet.created_at
                                else None
                            ),
                            "author_id": tweet.author_id,
                            "metrics": {
                                "retweet_count": tweet.public_metrics.get(
                                    "retweet_count", 0
                                ),
                                "like_count": tweet.public_metrics.get("like_count", 0),
                                "reply_count": tweet.public_metrics.get(
                                    "reply_count", 0
                                ),
                                "quote_count": tweet.public_metrics.get(
                                    "quote_count", 0
                                ),
                            },
                            "fetched_at": datetime.now().isoformat(),
                            "is_mention": True,
                        }
                    )

                self._save_tweets_to_json(formatted, "reg_mentions")
                return formatted
        except Exception as e:
            logger.error(f"Error fetching mentions: {e}")
            return []

    def _save_tweets_to_json(self, tweets: List[Dict], username: str):
        """Save tweet data to timestamped JSON file."""
        try:
            os.makedirs("data", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data/{username}_tweets_{timestamp}.json"

            with open(filename, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "username": username,
                        "fetched_at": datetime.now().isoformat(),
                        "tweet_count": len(tweets),
                        "tweets": tweets,
                    },
                    f,
                    indent=2,
                    ensure_ascii=False,
                    default=str,
                )

            logger.info(f"Saved {len(tweets)} tweets to {filename}")

        except Exception as e:
            logger.error(f"Error saving tweets to JSON: {e}")

    def process_tweets(self, tweets: List[Dict]) -> List[Outage]:
        outages = []

        for tweet in tweets:
            if tweet.get("is_mention"):
                tweet_text = tweet.get("text", "")
                outage = self.extractor.process_tweet(
                    tweet_text, tweet_id=str(tweet["id"])
                )
            else:
                reg_text = tweet.get("text", "")
                user_text = tweet.get("original_user_text")
                outage = self.extractor.process_tweet(
                    reg_text,
                    tweet_id=str(tweet["id"]),
                    user_text=user_text,
                )

            if outage:
                outage.timestamp = tweet.get("created_at")
                outages.append(outage)
        return outages

    def _get_last_processed_id(self, filename: str) -> Optional[str]:
        try:
            with open(filename, "r") as f:
                return f.read().strip()
        except FileNotFoundError:
            return None

    def _set_last_processed_id(self, filename: str, tweet_id: str):
        with open(filename, "w") as f:
            f.write(tweet_id)


def main():
    twitter_config = TwitterConfig(
        bearer_token=settings.BEARER_TOKEN,
        consumer_key=settings.CONSUMER_KEY,
        consumer_secret=settings.CONSUMER_SECRET,
        access_token=settings.ACCESS_TOKEN,
        access_token_secret=settings.ACCESS_TOKEN_SECRET,
    )
    twitter_client = TwitterClient(config=twitter_config)
    tweets = twitter_client.fetch_reg_tweets()
    print(tweets)


# if __name__ == "__main__":
#     main()
