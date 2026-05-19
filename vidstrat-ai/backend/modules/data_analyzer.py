from datetime import datetime
from typing import Dict, List

import numpy as np


class DataAnalyzer:
    DIMENSIONS = ["consistency", "engagement", "audience_growth", "content_performance", "activity_level", "overall_strength"]

    @staticmethod
    def _parse_dates(upload_dates: List[str]) -> List[datetime]:
        parsed = []
        for date in upload_dates or []:
            try:
                parsed.append(datetime.fromisoformat(date.replace("Z", "+00:00")))
            except Exception:
                continue
        return sorted(parsed, reverse=True)

    def calculate_posting_consistency(self, upload_dates: List[str]) -> Dict:
        dates = self._parse_dates(upload_dates)
        if len(dates) < 2:
            return {"score": 0, "avg_interval_days": 0, "std_dev": 0, "classification": "Sporadic"}
        intervals = [(dates[index] - dates[index + 1]).days for index in range(len(dates) - 1)]
        avg_interval = float(np.mean(intervals))
        std_dev = float(np.std(intervals))
        score = max(0, 100 - std_dev * 2)
        if score > 80:
            classification = "Very Consistent"
        elif score >= 60:
            classification = "Consistent"
        elif score >= 40:
            classification = "Irregular"
        else:
            classification = "Sporadic"
        return {
            "score": round(score, 1),
            "avg_interval_days": round(avg_interval, 1),
            "std_dev": round(std_dev, 1),
            "classification": classification,
        }

    @staticmethod
    def calculate_growth_velocity(videos: List[Dict]) -> Dict:
        recent = sorted(videos, key=lambda video: video.get("published_at", ""), reverse=True)
        if len(recent) < 12:
            return {"percentage_change": 0, "trend": "Insufficient data"}
        last_10 = np.mean([video.get("views", 0) for video in recent[:10]])
        previous_set = recent[10:20] if len(recent) >= 20 else recent[10:]
        previous_10 = np.mean([video.get("views", 0) for video in previous_set])
        change = ((last_10 - previous_10) / previous_10 * 100) if previous_10 else 0
        return {"percentage_change": round(float(change), 1), "trend": "Rising" if change > 5 else "Declining" if change < -5 else "Flat"}

    @staticmethod
    def detect_outlier_videos(videos: List[Dict]) -> List[Dict]:
        views = np.array([video.get("views", 0) for video in videos], dtype=float)
        if len(views) < 3 or float(np.std(views)) == 0:
            return []
        mean = float(np.mean(views))
        std_dev = float(np.std(views))
        outliers = []
        for video in videos:
            z_score = (video.get("views", 0) - mean) / std_dev
            if video.get("views", 0) > mean + 1.5 * std_dev:
                outliers.append({**video, "z_score": round(float(z_score), 2)})
        return sorted(outliers, key=lambda video: video["z_score"], reverse=True)[:6]

    @staticmethod
    def _engagement_score(rate: float) -> float:
        return min(100, max(0, rate / 4 * 100))

    @staticmethod
    def _activity_score(videos_per_month: float) -> int:
        if videos_per_month < 1:
            return 20
        if videos_per_month < 2:
            return 40
        if videos_per_month < 4:
            return 60
        if videos_per_month < 8:
            return 80
        return 100

    def calculate_radar_scores(self, channel_data: Dict, all_channel_data: List[Dict]) -> Dict:
        consistency_meta = self.calculate_posting_consistency(channel_data.get("upload_dates", []))
        subscribers = channel_data.get("subscribers", 0)
        avg_views = channel_data.get("avg_views", 0)
        views_per_subscriber = (avg_views / subscribers * 100) if subscribers else 0
        dates = self._parse_dates(channel_data.get("upload_dates", []))
        if len(dates) >= 2:
            months = max(1, (dates[0] - dates[-1]).days / 30)
            videos_per_month = len(dates) / months
        else:
            videos_per_month = 0
        ordered_subscribers = sorted({company.get("subscribers", 0) for company in all_channel_data})
        if len(ordered_subscribers) <= 1:
            audience_growth = 70
        else:
            audience_growth = 40 + (ordered_subscribers.index(subscribers) / (len(ordered_subscribers) - 1)) * 60
        scores = {
            "consistency": round(consistency_meta["score"], 1),
            "engagement": round(self._engagement_score(channel_data.get("avg_engagement_rate", 0)), 1),
            "audience_growth": round(audience_growth, 1),
            "content_performance": round(min(100, views_per_subscriber * 10), 1),
            "activity_level": self._activity_score(videos_per_month),
        }
        overall = (
            scores["consistency"] * 0.2
            + scores["engagement"] * 0.25
            + scores["audience_growth"] * 0.15
            + scores["content_performance"] * 0.25
            + scores["activity_level"] * 0.15
        )
        scores["overall_strength"] = round(overall, 1)
        scores["consistency_meta"] = consistency_meta
        scores["growth_velocity"] = self.calculate_growth_velocity(channel_data.get("videos", []))
        return scores

    def compare_all_companies(self, all_channel_data: List[Dict]) -> Dict:
        valid = [company for company in all_channel_data if not company.get("error")]
        scores = {company["name"]: self.calculate_radar_scores(company, valid) for company in valid}
        ranked = sorted(scores.items(), key=lambda item: item[1]["overall_strength"], reverse=True)
        final_ranking = []
        for rank, (company, score) in enumerate(ranked, start=1):
            dimensions = {key: value for key, value in score.items() if key in self.DIMENSIONS[:-1]}
            key_strength = max(dimensions, key=dimensions.get).replace("_", " ").title()
            biggest_opportunity = min(dimensions, key=dimensions.get).replace("_", " ").title()
            final_ranking.append({
                "rank": rank,
                "company": company,
                "overall_score": score["overall_strength"],
                "key_strength": key_strength,
                "biggest_opportunity": biggest_opportunity,
            })
        return {
            "scores": scores,
            "ranked": final_ranking,
            "winner": ranked[0][0] if ranked else None,
        }
