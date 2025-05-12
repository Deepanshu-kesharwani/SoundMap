
import aiohttp
from typing import List, Dict


async def fetch_youtube_video(query: str, api_key: str) -> List[Dict[str, str]]:
    try:
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "key": api_key,
            "maxResults": 5
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    videos = data.get("items", [])
                    return [
                        {
                            "title": video["snippet"]["title"],
                            "videoId": video["id"]["videoId"],
                            "thumbnail": video["snippet"]["thumbnails"]["default"]["url"]
                        }
                        for video in videos
                    ]
                return []
    except Exception:
        return []


async def fetch_lastfm_recommendations(query: str, api_key: str) -> List[Dict[str, str]]:
    try:
        url = "http://ws.audioscrobbler.com/2.0/"
        params = {
            "method": "artist.search",
            "artist": query,
            "api_key": api_key,
            "format": "json",
            "limit": 10
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    artists = data.get("results", {}).get("artistmatches", {}).get("artist", [])
                    return [{"name": artist["name"]} for artist in artists]
                return []
    except Exception:
        return []


async def fetch_lastfm_user_recommendations(username: str, api_key: str) -> List[Dict[str, str]]:
    try:
        url = "http://ws.audioscrobbler.com/2.0/"
        params = {
            "method": "user.gettopartists",
            "user": username,
            "api_key": api_key,
            "format": "json",
            "limit": 10
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    artists = data.get("topartists", {}).get("artist", [])
                    return [{"name": artist["name"], "playcount": artist["playcount"]} for artist in artists]
                return []
    except Exception:
        return []
