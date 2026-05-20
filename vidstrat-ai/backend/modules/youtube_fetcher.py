import os
import re
from typing import Dict, List, Optional, Tuple

import isodate
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from modules import cache


class YouTubeFetcher:
    KNOWN_CHANNEL_IDS = {
        "mrbeast": ("UCX6OQ3DkcsbYNE6H8uQQuVA", "MrBeast"),
        "mr beast": ("UCX6OQ3DkcsbYNE6H8uQQuVA", "MrBeast"),
        "pewdiepie": ("UC-lHJZR3Gqxm24_Vd_AJ5Yw", "PewDiePie"),
        "pew die pie": ("UC-lHJZR3Gqxm24_Vd_AJ5Yw", "PewDiePie"),
        "dudeperfect": ("UCRijo3ddMTht_IHyNSNXpNQ", "Dude Perfect"),
        "dude perfect": ("UCRijo3ddMTht_IHyNSNXpNQ", "Dude Perfect"),
        "mkbhd": ("UCBJycsmduvYEL83R_U4JriQ", "Marques Brownlee"),
        "marques brownlee": ("UCBJycsmduvYEL83R_U4JriQ", "Marques Brownlee"),
        "puma": ("UCZq427EjGqUbV6pZIjEKkgg", "PUMA"),
    }

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("YOUTUBE_API_KEY")
        if not self.api_key:
            raise ValueError("Missing YOUTUBE_API_KEY. Add it to backend/.env.")
        self.youtube = build("youtube", "v3", developerKey=self.api_key, cache_discovery=False)

    @staticmethod
    def friendly_error(error: Exception, company_name: str = "") -> str:
        text = str(error).lower()
        if isinstance(error, HttpError):
            if "quota" in text:
                return "YouTube API quota has been reached. Please try again tomorrow or use a different API key."
            if any(term in text for term in ["api key not valid", "bad request", "keyinvalid"]):
                return "The configured YouTube API key is invalid. Add a valid YouTube Data API v3 key to backend/.env and restart the backend."
            if any(term in text for term in ["access not configured", "has not been used", "disabled", "forbidden", "permission"]):
                return "The configured API key cannot access YouTube Data API v3. Enable YouTube Data API v3 for that Google Cloud project, check API restrictions, then restart the backend."
            return f"YouTube API error: {getattr(error, 'reason', None) or str(error)}"
        if "quota" in text:
            return "YouTube API quota has been reached. Please try again tomorrow or use a different API key."
        if any(term in text for term in ["connection", "timeout", "network", "name resolution"]):
            return "Connection failed. Please check your connection and try again."
        if company_name:
            return f"Could not locate an official YouTube channel for {company_name}. This company will be excluded from the analysis."
        return "Connection failed. Please check your connection and try again."

    @staticmethod
    def _normalize_name(value: str) -> str:
        return " ".join(re.findall(r"[a-z0-9]+", value.lower()))

    @classmethod
    def _known_channel(cls, company_name: str) -> Optional[Tuple[str, str]]:
        normalized = cls._normalize_name(company_name)
        compact = normalized.replace(" ", "")
        return cls.KNOWN_CHANNEL_IDS.get(normalized) or cls.KNOWN_CHANNEL_IDS.get(compact)

    @staticmethod
    def _safe_int(value) -> int:
        try:
            return int(value or 0)
        except (TypeError, ValueError):
            return 0

    def search_channel(self, company_name: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        known = self._known_channel(company_name)
        if known:
            return known[0], known[1], None

        try:
            candidates = {}
            for query in self._channel_queries(company_name):
                response = self.youtube.search().list(
                    part="snippet",
                    q=query,
                    type="channel",
                    order="relevance",
                    maxResults=10,
                ).execute()
                for item in response.get("items", []):
                    channel_id = item.get("snippet", {}).get("channelId")
                    if channel_id:
                        candidates[channel_id] = item
            if not candidates:
                return None, None, f"Could not locate an official YouTube channel for {company_name}. This company will be excluded from the analysis."
            stats_by_id = self.get_channel_stats_batch(list(candidates.keys()))
            item = max(
                candidates.values(),
                key=lambda candidate: self._channel_match_score(
                    company_name,
                    candidate,
                    stats_by_id.get(candidate.get("snippet", {}).get("channelId"), {}),
                ),
            )
            return item["snippet"]["channelId"], item["snippet"]["title"], None
        except Exception as error:
            return None, None, self.friendly_error(error, company_name)

    @staticmethod
    def _channel_queries(company_name: str) -> List[str]:
        cleaned = " ".join(company_name.split())
        return [
            f"{cleaned} official YouTube channel",
            f"{cleaned} official",
            cleaned,
        ]

    @staticmethod
    def _channel_match_score(company_name: str, candidate: Dict, stats: Optional[Dict] = None) -> float:
        stats = stats or {}
        title = candidate.get("snippet", {}).get("title", "")
        description = candidate.get("snippet", {}).get("description", "")
        title_tokens = set(re.findall(r"[a-z0-9]+", title.lower()))
        company_tokens = set(re.findall(r"[a-z0-9]+", company_name.lower()))
        normalized_title = re.sub(r"[^a-z0-9]+", "", title.lower())
        normalized_company = re.sub(r"[^a-z0-9]+", "", company_name.lower())
        score = len(title_tokens & company_tokens) * 20
        lower_title = title.lower()
        lower_description = description.lower()
        if normalized_company and normalized_title == normalized_company:
            score += 120
        elif normalized_company and normalized_company in normalized_title:
            score += 55
        if company_name.lower() in lower_description:
            score += 15
        if "official" in lower_title:
            score += 20
        if "india" in lower_title:
            score += 8
        if "tv" in lower_title:
            score += 6
        subscribers = YouTubeFetcher._safe_int(stats.get("subscriberCount"))
        views = YouTubeFetcher._safe_int(stats.get("viewCount"))
        videos = YouTubeFetcher._safe_int(stats.get("videoCount"))
        score += min(80, subscribers / 25_000)
        score += min(35, views / 5_000_000)
        if subscribers < 1_000:
            score -= 80
        if videos < 3:
            score -= 20
        return score

    def get_channel_stats_batch(self, channel_ids: List[str]) -> Dict[str, Dict]:
        results: Dict[str, Dict] = {}
        for index in range(0, len(channel_ids), 50):
            batch = channel_ids[index:index + 50]
            response = self.youtube.channels().list(
                part="statistics",
                id=",".join(batch),
                maxResults=50,
            ).execute()
            for item in response.get("items", []):
                results[item["id"]] = item.get("statistics", {})
        return results

    def get_channel_stats(self, channel_id: str) -> Dict:
        response = self.youtube.channels().list(
            part="snippet,statistics,brandingSettings",
            id=channel_id,
            maxResults=1,
        ).execute()
        items = response.get("items", [])
        if not items:
            raise ValueError("Channel details were not returned by YouTube.")
        item = items[0]
        snippet = item.get("snippet", {})
        stats = item.get("statistics", {})
        branding = item.get("brandingSettings", {}).get("channel", {})
        thumbs = snippet.get("thumbnails", {})
        thumbnail = (thumbs.get("high") or thumbs.get("medium") or thumbs.get("default") or {}).get("url", "")
        # fallback: construct a reasonable channel thumbnail if YouTube didn't provide one
        if not thumbnail:
            thumbnail = f"https://yt3.ggpht.com/ytc/AKedOLT{channel_id}=s96-c"
        return {
            "channel_id": channel_id,
            "channel_title": snippet.get("title", ""),
            "subscribers": self._safe_int(stats.get("subscriberCount")) if not stats.get("hiddenSubscriberCount") else 0,
            "hidden_subscribers": bool(stats.get("hiddenSubscriberCount")),
            "total_views": self._safe_int(stats.get("viewCount")),
            "video_count": self._safe_int(stats.get("videoCount")),
            "country": snippet.get("country") or branding.get("country", ""),
            "description": snippet.get("description", ""),
            "published_at": snippet.get("publishedAt", ""),
            "custom_url": snippet.get("customUrl", ""),
            "thumbnail_url": thumbnail,
        }

    def get_recent_videos(self, channel_id: str, max_results: int = 50) -> List[Dict]:
        response = self.youtube.search().list(
            part="snippet",
            channelId=channel_id,
            type="video",
            order="date",
            maxResults=max_results,
        ).execute()
        videos = []
        for item in response.get("items", []):
            snippet = item.get("snippet", {})
            thumbs = snippet.get("thumbnails", {})
            thumbnail = (thumbs.get("medium") or thumbs.get("default") or {}).get("url", "")
            # fallback: use standard YouTube thumbnail URL pattern when snippet thumbnails are missing
            if not thumbnail:
                video_id = item.get("id", {}).get("videoId")
                if video_id:
                    thumbnail = f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"
            videos.append({
                "video_id": item.get("id", {}).get("videoId"),
                "title": snippet.get("title", ""),
                "published_at": snippet.get("publishedAt", ""),
                "description": snippet.get("description", ""),
                "tags": [],
                "thumbnail_url": thumbnail,
            })
        return [video for video in videos if video.get("video_id")]

    def get_video_stats(self, video_ids: List[str]) -> Dict[str, Dict]:
        results: Dict[str, Dict] = {}
        for index in range(0, len(video_ids), 50):
            batch = video_ids[index:index + 50]
            response = self.youtube.videos().list(
                part="statistics,contentDetails,snippet",
                id=",".join(batch),
                maxResults=50,
            ).execute()
            for item in response.get("items", []):
                stats = item.get("statistics", {})
                content = item.get("contentDetails", {})
                snippet = item.get("snippet", {})
                views = self._safe_int(stats.get("viewCount"))
                likes = self._safe_int(stats.get("likeCount"))
                comments = self._safe_int(stats.get("commentCount"))
                duration_seconds = int(isodate.parse_duration(content.get("duration", "PT0S")).total_seconds())
                results[item["id"]] = {
                    "views": views,
                    "likes": likes,
                    "comments": comments,
                    "duration_seconds": duration_seconds,
                    "definition": content.get("definition", "").upper(),
                    "caption": content.get("caption", "false") == "true",
                    "tags": snippet.get("tags", []),
                    "engagement_rate": ((likes + comments) / views * 100) if views else 0,
                }
        return results

    def get_full_channel_data(self, company_name: str) -> Dict:
        cache_key = f"channel-v2:{self._normalize_name(company_name)}"
        cached = cache.load_cached_channel(cache_key)
        if cached:
            return cached

        channel_id, found_title, error = self.search_channel(company_name)
        if error:
            return {"name": company_name, "error": error, "videos": []}
        try:
            channel = self.get_channel_stats(channel_id)
            raw_videos = self.get_recent_videos(channel_id)
            stats_by_id = self.get_video_stats([video["video_id"] for video in raw_videos])
            videos = [{**video, **stats_by_id.get(video["video_id"], {})} for video in raw_videos]
            videos.sort(key=lambda item: item.get("views", 0), reverse=True)

            def avg(key: str) -> float:
                return sum(video.get(key, 0) for video in videos) / len(videos) if videos else 0

            channel.update({
                "name": company_name,
                "found_title": found_title,
                "videos": videos,
                "avg_views": avg("views"),
                "avg_engagement_rate": avg("engagement_rate"),
                "avg_likes": avg("likes"),
                "avg_comments": avg("comments"),
                "top_5_videos": videos[:5],
                "recent_10_videos": sorted(videos, key=lambda video: video.get("published_at", ""), reverse=True)[:10],
                "upload_dates": [video.get("published_at", "") for video in raw_videos if video.get("published_at")],
            })
            cache.save_cached_channel(cache_key, channel)
            return channel
        except Exception as error:
            if cached:
                return cached
            return {"name": company_name, "error": self.friendly_error(error, company_name), "videos": []}
