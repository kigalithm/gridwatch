from app.reg.twitter.twitter_client import TwitterClient
from app.reg.schema.outage_schema import (
    TwitterConfig,
)
from fastapi import APIRouter, HTTPException


twitter_route = APIRouter(tags=["Twitter"])


@twitter_route.post("/config")
async def configure_twitter(config: TwitterConfig):
    """Configure Twitter API credentials"""
    global twitter_client
    try:
        twitter_client = TwitterClient(config)
        return {"message": "Twitter API configured successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Twitter configuration failed: {e}"
        )
