import os
import base64
import requests
from typing import Optional


GEMINI_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_BEARER = os.getenv('GEMINI_BEARER')
GEMINI_ENDPOINT = os.getenv('GEMINI_IMAGE_ENDPOINT') or 'https://generativelanguage.googleapis.com/v1/images:generate'


def _find_base64_in_response(obj) -> Optional[str]:
    """Recursively search for a plausible base64 image string in the parsed JSON response."""
    if not obj:
        return None
    if isinstance(obj, str):
        s = obj
        # crude check: reasonably long and only base64 chars plus padding
        if len(s) > 100 and all(c.isalnum() or c in '+/=\n\r' for c in s):
            return s
    if isinstance(obj, dict):
        for v in obj.values():
            found = _find_base64_in_response(v)
            if found:
                return found
    if isinstance(obj, list):
        for v in obj:
            found = _find_base64_in_response(v)
            if found:
                return found
    return None


def generate_image_base64(prompt: str, size: str = '512x512') -> Optional[str]:
    """Generate an image using Gemini / Google Generative Images endpoint.

    Tries API Key query parameter first; if `GEMINI_BEARER` present uses Authorization header.
    Returns raw base64 image string (no data: prefix) or None on failure.
    """
    if not GEMINI_KEY and not GEMINI_BEARER:
        return None

    payload = {
        "model": "image-bison-001",
        "prompt": prompt,
        "size": size,
    }

    headers = {"Content-Type": "application/json"}
    if GEMINI_BEARER:
        headers["Authorization"] = f"Bearer {GEMINI_BEARER}"

    # try with API key query param if we have one
    attempts = []
    try:
        if GEMINI_KEY:
            url = f"{GEMINI_ENDPOINT}?key={GEMINI_KEY}"
            resp = requests.post(url, json=payload, headers=headers, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            b64 = _find_base64_in_response(data)
            if b64:
                return b64
            attempts.append(data)

        # fallback: try without API key if bearer token present
        if GEMINI_BEARER:
            resp = requests.post(GEMINI_ENDPOINT, json=payload, headers=headers, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            b64 = _find_base64_in_response(data)
            if b64:
                return b64
            attempts.append(data)

        # nothing found
        return None
    except Exception:
        return None
