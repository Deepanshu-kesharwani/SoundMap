
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import redis.asyncio as redis
from pydantic import BaseModel
import json
import os
from dotenv import load_dotenv
from services import (
    fetch_youtube_video,
    fetch_lastfm_recommendations,
    fetch_lastfm_user_recommendations
)
from redis_setup import redis_client
load_dotenv()

LASTFM_API_KEY = os.getenv("LASTFM_API_KEY", "YOUR_LASTFM_API_KEY")
LASTFM_USERNAME = os.getenv("LASTFM_USERNAME", "YOUR_LASTFM_USERNAME")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "YOUR_YOUTUBE_API_KEY")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))



app = FastAPI(title="SoundMap API")

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchQuery(BaseModel):
    query: str

@app.get("/")
async def root():
    return {"message": "Welcome to SoundMap API"}

@app.post("/search")
async def search_music(query: SearchQuery):
    try:
        cache_key = f"search:{query.query}"
        cached_result = await redis_client.get(cache_key)
        if cached_result:
            return json.loads(cached_result)

        youtube_results = await fetch_youtube_video(query.query, YOUTUBE_API_KEY) or []
        lastfm_results = await fetch_lastfm_recommendations(query.query, LASTFM_API_KEY) or []
        user_recommendations = await fetch_lastfm_user_recommendations(LASTFM_USERNAME, LASTFM_API_KEY) or []

        response = {
            "youtube": youtube_results,
            "lastfm": lastfm_results,
            "user_recommendations": user_recommendations
        }

        await redis_client.setex(cache_key, 3600, json.dumps(response))
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")