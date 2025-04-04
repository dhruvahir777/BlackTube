from fastapi import FastAPI
import yt_dlp
import asyncio

# ✅ FastAPI App Create
app = FastAPI()

# ✅ Function to fetch video info
def fetch_video_data(query, max_results=5):
    search_url = f"ytsearch{max_results}:{query}"
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'nocheckcertificate': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(search_url, download=False)

# ✅ Function to clean video data
def clean_video_data(video):
    return {
        "id": video.get("id"),
        "title": video.get("title"),
        "description": video.get("description"),
        "uploader": video.get("uploader"),
        "upload_date": video.get("upload_date"),
        "duration": video.get("duration"),
        "view_count": video.get("view_count"),
        "like_count": video.get("like_count"),
        "tags": video.get("tags"),
        "categories": video.get("categories"),
        "is_live": video.get("is_live"),
        "age_limit": video.get("age_limit"),
        "thumbnail": video.get("thumbnail")
    }

# ✅ API Route for Searching Videos
@app.get("/search")
async def search_videos(query: str):
    raw_data = await asyncio.to_thread(fetch_video_data, query)
    entries = raw_data.get("entries", [])
    return [clean_video_data(video) for video in entries]

# ✅ Root Route (Optional)
@app.get("/")
def home():
    return {"message": "YouTube Search API is Running!"}
