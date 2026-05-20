import os
from datetime import datetime, timedelta
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from modules.ai_analyzer import AIAnalyzer
from modules.chart_generator import ChartGenerator
from modules.data_analyzer import DataAnalyzer
from modules.pptx_builder import PPTXBuilder
from modules.seo_analyzer import SEOAnalyzer
from modules.youtube_fetcher import YouTubeFetcher
from modules import cache
from fastapi.staticfiles import StaticFiles

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"), override=True)

app = FastAPI(title="anvidAI Video Marketing Intelligence API", version="1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ensure cache/static dirs exist and mount static files for thumbnails
cache.ensure_dirs()
static_dir = os.path.join(os.path.dirname(__file__), 'static')
if not os.path.exists(static_dir):
    os.makedirs(static_dir, exist_ok=True)
    os.makedirs(os.path.join(static_dir, 'thumbs'), exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")


class AnalyseRequest(BaseModel):
    primary_company: str = Field(..., min_length=1)
    competitors: List[str] = Field(default_factory=list, max_length=4)


@app.get("/api/health")
def health():
    return {"status": "ok", "version": "1.0"}


@app.post("/api/analyse")
def analyse(request: AnalyseRequest):
    names = [request.primary_company.strip()] + [name.strip() for name in request.competitors if name.strip()]
    if not request.primary_company.strip():
        raise HTTPException(status_code=400, detail="Enter at least one YouTube channel or company name.")

    try:
        fetcher = YouTubeFetcher()
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error

    raw_channels = [fetcher.get_full_channel_data(name) for name in names]
    valid_channels = [channel for channel in raw_channels if not channel.get("error")]
    live_errors = [{"name": channel.get("name"), "error": channel.get("error")} for channel in raw_channels if channel.get("error")]
    if len(valid_channels) < 1:
        unique_errors = list(dict.fromkeys(error["error"] for error in live_errors if error.get("error")))
        details = " ".join(unique_errors) or "Could not fetch enough valid YouTube channels."
        raise HTTPException(status_code=503, detail=f"Live YouTube data is unavailable: {details}")

    data_analyzer = DataAnalyzer()
    seo_analyzer = SEOAnalyzer()
    ai_analyzer = AIAnalyzer()
    chart_generator = ChartGenerator()

    comparison = data_analyzer.compare_all_companies(valid_channels)
    seo_by_company = {channel["name"]: seo_analyzer.analyze_company(channel) for channel in valid_channels}
    pillar_by_company = {channel["name"]: ai_analyzer.classify_content_pillars(channel.get("videos", [])) for channel in valid_channels}

    companies = []
    for channel in valid_channels:
        name = channel["name"]
        radar_scores = comparison["scores"][name]
        persona = ai_analyzer.generate_channel_persona(name, channel, radar_scores)
        top_videos = []
        for video in channel.get("top_5_videos", []):
            top_videos.append({
                "title": video.get("title", ""),
                "views": video.get("views", 0),
                "likes": video.get("likes", 0),
                "comments": video.get("comments", 0),
                "thumbnail_url": video.get("thumbnail_url", ""),
                "engagement_rate": round(video.get("engagement_rate", 0), 2),
                "published_at": video.get("published_at", ""),
                "why_it_worked": f"This video over-indexed because it combines clear audience intent with a format already validated by {name}'s strongest view signals.",
            })
        steal_strategy = ai_analyzer.generate_steal_this_strategy(name, top_videos[0] if top_videos else {}, channel)
        # choose a channel thumbnail, fall back to the first recent video's thumbnail if missing
        channel_thumbnail = channel.get("thumbnail_url") or (channel.get("videos")[0].get("thumbnail_url") if channel.get("videos") else "")

        companies.append({
            "name": name,
            "channel_title": channel.get("channel_title", ""),
            "thumbnail_url": channel_thumbnail or "",
            "subscribers": channel.get("subscribers", 0),
            "total_views": channel.get("total_views", 0),
            "video_count": channel.get("video_count", 0),
            "avg_views": round(channel.get("avg_views", 0), 1),
            "avg_engagement_rate": round(channel.get("avg_engagement_rate", 0), 2),
            "avg_likes": round(channel.get("avg_likes", 0), 1),
            "avg_comments": round(channel.get("avg_comments", 0), 1),
            "consistency_score": radar_scores["consistency_meta"]["score"],
            "consistency_classification": radar_scores["consistency_meta"]["classification"],
            "avg_interval_days": radar_scores["consistency_meta"]["avg_interval_days"],
            "radar_scores": {key: radar_scores[key] for key in DataAnalyzer.DIMENSIONS},
            "seo_scores": seo_by_company[name],
            "content_pillars": pillar_by_company[name],
            "top_videos": top_videos,
            "videos_over_time": sorted([{"date": video.get("published_at", "")[:10], "views": video.get("views", 0)} for video in channel.get("videos", [])], key=lambda item: item["date"])[-25:],
            "upload_day_distribution": seo_by_company[name]["day_distribution"],
            "outlier_videos": data_analyzer.detect_outlier_videos(channel.get("videos", [])),
            "format_distribution": format_distribution(channel.get("videos", [])),
            "persona": persona,
            "steal_strategy": steal_strategy,
        })

    score_map = {company["name"]: company["radar_scores"] for company in companies}
    charts = {
        "radar_base64": chart_generator.generate_radar_chart(score_map),
        "scatter_base64": chart_generator.generate_engagement_scatter(valid_channels),
        "pillars_base64": chart_generator.generate_content_pillar_chart(pillar_by_company),
        "cadence_base64": chart_generator.generate_cadence_chart({company["name"]: company["upload_day_distribution"] for company in companies}),
    }
    executive_verdict = ai_analyzer.generate_executive_verdict(valid_channels, comparison["scores"], comparison["winner"])
    whitespace = ai_analyzer.generate_whitespace_analysis(valid_channels)
    action_plan = ai_analyzer.generate_90_day_plan(request.primary_company.strip(), {
        "companies": companies,
        "ranking": comparison["ranked"],
        "whitespace": whitespace,
    })

    payload = {
        "companies": companies,
        "winner": comparison["winner"],
        "executive_verdict": executive_verdict,
        "whitespace_opportunities": whitespace,
        "action_plan": action_plan,
        "final_ranking": comparison["ranked"],
        "charts": charts,
        "pptx_base64": "",
        "total_videos_analysed": sum(len(channel.get("videos", [])) for channel in valid_channels),
        "excluded_companies": [{"name": channel.get("name"), "error": channel.get("error")} for channel in raw_channels if channel.get("error")],
        "live_errors": live_errors,
        "ai_available": ai_analyzer.available,
        "ai_message": "AI commentary disabled because no Anthropic API key is configured.",
        "data_source": "youtube",
    }
    if ai_analyzer.available:
        payload["ai_message"] = "AI commentary is enabled."
    payload["pptx_base64"] = PPTXBuilder().build_report(payload)
    return payload


def format_distribution(videos):
    buckets = {"Shorts": 0, "Mid-length": 0, "Long-form": 0}
    for video in videos:
        seconds = int(video.get("duration_seconds", 0) or 0)
        if seconds <= 60:
            buckets["Shorts"] += 1
        elif seconds <= 600:
            buckets["Mid-length"] += 1
        else:
            buckets["Long-form"] += 1
    return buckets


def generate_demo_channel_data(company_name: str, index: int) -> dict:
    seed = sum(ord(char) for char in company_name) + index * 41
    base_subscribers = 240_000 + (seed % 850_000) + index * 130_000
    base_views = 18_000 + (seed % 45_000) + index * 9_000
    today = datetime.utcnow().replace(microsecond=0)
    videos = []
    topics = [
        "Brand story and trust",
        "Product launch highlights",
        "Recipe ideas for families",
        "Festival campaign",
        "Behind the process",
        "Customer moments",
        "How to choose the right product",
        "Quality promise explained",
        "Shorts trend response",
        "Nutrition tips",
    ]
    for video_index in range(24):
        interval = 4 + ((seed + video_index + index) % 5)
        published = today - timedelta(days=video_index * interval + index)
        views = base_views + ((video_index * 7919 + seed) % 110_000)
        if video_index in (2, 9):
            views = int(views * 2.4)
        likes = int(views * (0.018 + ((seed + video_index) % 15) / 1000))
        comments = int(views * (0.0018 + ((seed + video_index) % 5) / 10000))
        videos.append({
            "video_id": f"demo-{index}-{video_index}",
            "title": f"{company_name}: {topics[video_index % len(topics)]}",
            "published_at": published.isoformat() + "Z",
            "description": f"{company_name} video about {topics[video_index % len(topics)].lower()} with product details, audience value, campaign links, and category context.",
            "tags": [company_name, "brand", "youtube strategy"],
            "thumbnail_url": "",
            "views": views,
            "likes": likes,
            "comments": comments,
            "duration_seconds": 35 + ((seed + video_index * 53) % 900),
            "definition": "HD",
            "caption": video_index % 3 == 0,
            "engagement_rate": ((likes + comments) / views * 100) if views else 0,
        })
    videos.sort(key=lambda item: item.get("views", 0), reverse=True)

    def avg(key: str) -> float:
        return sum(video.get(key, 0) for video in videos) / len(videos) if videos else 0

    safe_name = company_name.replace(" ", "_")
    return {
        "channel_id": f"demo-{safe_name.lower()}",
        "channel_title": company_name,
        "subscribers": base_subscribers,
        "hidden_subscribers": False,
        "total_views": base_views * 180,
        "video_count": 90 + (seed % 220),
        "country": "IN",
        "description": f"Demo channel data for {company_name}.",
        "published_at": "2015-01-01T00:00:00Z",
        "custom_url": f"@{safe_name}",
        "thumbnail_url": f"/static/thumbs/channel_{safe_name}.jpg",
        "name": company_name,
        "found_title": company_name,
        "videos": videos,
        "avg_views": avg("views"),
        "avg_engagement_rate": avg("engagement_rate"),
        "avg_likes": avg("likes"),
        "avg_comments": avg("comments"),
        "top_5_videos": videos[:5],
        "recent_10_videos": sorted(videos, key=lambda video: video.get("published_at", ""), reverse=True)[:10],
        "upload_dates": [video.get("published_at", "") for video in videos],
    }


frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "dist"))
if os.path.exists(os.path.join(frontend_dist, "index.html")):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="frontend")
