import os
import json
import hashlib
from typing import Optional


CACHE_DIR = os.path.join(os.path.dirname(__file__), '..', 'cache')
THUMBS_DIR = os.path.join(os.path.dirname(__file__), '..', 'static', 'thumbs')


def ensure_dirs():
    os.makedirs(CACHE_DIR, exist_ok=True)
    os.makedirs(THUMBS_DIR, exist_ok=True)


def cache_path_for_key(key: str) -> str:
    ensure_dirs()
    h = hashlib.sha1(key.encode('utf-8')).hexdigest()
    return os.path.join(CACHE_DIR, f"{h}.json")


def load_cached_channel(key: str) -> Optional[dict]:
    path = cache_path_for_key(key)
    if not os.path.exists(path):
        return None
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            return json.load(fh)
    except Exception:
        return None


def save_cached_channel(key: str, data: dict):
    path = cache_path_for_key(key)
    try:
        with open(path, 'w', encoding='utf-8') as fh:
            json.dump(data, fh)
    except Exception:
        pass


def thumb_file_path_for_video(video_id: str) -> str:
    ensure_dirs()
    return os.path.join(THUMBS_DIR, f"{video_id}.jpg")


def thumb_url_for_video(video_id: str) -> str:
    # served at /static/thumbs/<id>.jpg
    return f"/static/thumbs/{video_id}.jpg"


def thumb_exists(video_id: str) -> bool:
    return os.path.exists(thumb_file_path_for_video(video_id))


def save_thumb_bytes(video_id: str, b: bytes):
    try:
        with open(thumb_file_path_for_video(video_id), 'wb') as fh:
            fh.write(b)
    except Exception:
        pass
