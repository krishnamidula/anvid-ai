import re
from collections import Counter
from datetime import datetime
from typing import Dict, List

import numpy as np


class SEOAnalyzer:
    POWER_WORDS = ["best", "how to", "guide", "tips", "secrets", "proven", "ultimate", "complete", "top", "review", "vs", "comparison", "tutorial", "step by step", "beginners"]

    def analyze_titles(self, videos: List[Dict]) -> Dict:
        titles = [video.get("title", "") for video in videos if video.get("title")]
        if not titles:
            return {"avg_title_length": 0, "number_titles_pct": 0, "question_titles_pct": 0, "power_word_score": 0, "title_score": 0}
        avg_length = float(np.mean([len(title) for title in titles]))
        number_pct = sum(bool(re.search(r"\d", title)) for title in titles) / len(titles) * 100
        question_pct = sum("?" in title for title in titles) / len(titles) * 100
        power_score = sum(any(word in title.lower() for word in self.POWER_WORDS) for title in titles) / len(titles) * 100
        length_score = 100 if 45 <= avg_length <= 75 else max(20, 100 - abs(avg_length - 60))
        title_score = length_score * 0.45 + power_score * 0.35 + min(100, number_pct + question_pct) * 0.2
        return {
            "avg_title_length": round(avg_length, 1),
            "number_titles_pct": round(number_pct, 1),
            "question_titles_pct": round(question_pct, 1),
            "power_word_score": round(power_score, 1),
            "title_score": round(title_score, 1),
        }

    @staticmethod
    def analyze_descriptions(videos: List[Dict]) -> Dict:
        descriptions = [video.get("description", "") or "" for video in videos]
        if not descriptions:
            return {"avg_description_length": 0, "links_pct": 0, "hashtags_pct": 0, "description_score": 0}
        avg_length = float(np.mean([len(description) for description in descriptions]))
        if avg_length == 0:
            score = 0
        elif avg_length < 100:
            score = 20
        elif avg_length < 300:
            score = 40
        elif avg_length < 500:
            score = 60
        elif avg_length < 1000:
            score = 80
        else:
            score = 100
        links_pct = sum(bool(re.search(r"https?://|www\.", description)) for description in descriptions) / len(descriptions) * 100
        hashtags_pct = sum("#" in description for description in descriptions) / len(descriptions) * 100
        return {"avg_description_length": round(avg_length, 1), "links_pct": round(links_pct, 1), "hashtags_pct": round(hashtags_pct, 1), "description_score": score}

    def analyze_upload_timing(self, upload_dates: List[str]) -> Dict:
        parsed = []
        for date in upload_dates or []:
            try:
                parsed.append(datetime.fromisoformat(date.replace("Z", "+00:00")))
            except Exception:
                continue
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        counts = Counter(date.strftime("%A") for date in parsed)
        distribution = {day: counts.get(day, 0) for day in days}
        best_day = max(distribution, key=distribution.get) if parsed else "N/A"
        timing_score = (max(distribution.values()) / len(parsed) * 100) if parsed else 0
        return {"day_distribution": distribution, "best_upload_day": best_day, "timing_score": round(timing_score, 1)}

    @staticmethod
    def calculate_overall_seo_score(title: Dict, desc: Dict, timing: Dict) -> float:
        return round(title.get("title_score", 0) * 0.4 + desc.get("description_score", 0) * 0.35 + timing.get("timing_score", 0) * 0.25, 1)

    def analyze_company(self, channel_data: Dict) -> Dict:
        titles = self.analyze_titles(channel_data.get("videos", []))
        descriptions = self.analyze_descriptions(channel_data.get("videos", []))
        timing = self.analyze_upload_timing(channel_data.get("upload_dates", []))
        return {**titles, **descriptions, **timing, "overall": self.calculate_overall_seo_score(titles, descriptions, timing)}
