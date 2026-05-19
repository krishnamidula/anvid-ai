import json
import os
import re
from typing import Dict, List

from anthropic import Anthropic


PILLARS = ["Education", "Product Showcase", "Entertainment", "Storytelling", "Behind-the-Scenes", "Social Proof", "Trend/Topical", "Tutorial/How-To", "Brand Culture"]


class AIAnalyzer:
    def __init__(self, api_key: str | None = None, model_name: str = "claude-sonnet-4-20250514"):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model_name = model_name
        self.available = bool(self.api_key)
        self.client = Anthropic(api_key=self.api_key) if self.available else None
        self.error = None

    @staticmethod
    def _compact_channel(channel_data: Dict) -> Dict:
        return {
            "company": channel_data.get("name"),
            "channel_title": channel_data.get("channel_title"),
            "subscribers": channel_data.get("subscribers"),
            "total_views": channel_data.get("total_views"),
            "avg_views": round(channel_data.get("avg_views", 0), 1),
            "avg_engagement_rate": round(channel_data.get("avg_engagement_rate", 0), 2),
            "top_titles": [video.get("title") for video in channel_data.get("top_5_videos", [])],
        }

    def _generate(self, prompt: str, fallback: str, max_tokens: int = 2000) -> str:
        if not self.available or not self.client:
            return fallback
        try:
            response = self.client.messages.create(
                model=self.model_name,
                max_tokens=max_tokens,
                temperature=0.55,
                system="You are a senior video marketing strategist at a top agency. Be specific, diagnostic, and commercially useful. Never use emojis.",
                messages=[{"role": "user", "content": prompt}],
            )
            return "".join(block.text for block in response.content if getattr(block, "type", "") == "text").strip()
        except Exception as error:
            self.available = False
            self.error = "AI analysis is currently unavailable. Data insights will be shown without strategic commentary."
            return fallback

    @staticmethod
    def _fallback_persona(company_name: str, channel_data: Dict, radar_scores: Dict) -> str:
        top_video = (channel_data.get("top_5_videos") or [{}])[0].get("title", "its strongest recent video")
        return f"{company_name} currently behaves like a channel optimized around proven demand signals rather than experimental audience development. Its audience relationship is strongest when content connects recognizable brand context with clear usefulness, as shown by {top_video}. Strategically, the channel should convert its best-performing formats into repeatable series while lifting weaker score dimensions such as {min(radar_scores, key=lambda key: radar_scores[key] if isinstance(radar_scores[key], (int, float)) else 100).replace('_', ' ')}."

    def generate_channel_persona(self, company_name: str, channel_data: Dict, radar_scores: Dict) -> str:
        prompt = f"""Write exactly 3 sentences profiling this YouTube channel. Cover content philosophy, audience relationship, and strategic intent. Use the actual metrics and avoid generic language.
Company: {company_name}
Channel data: {json.dumps(self._compact_channel(channel_data), ensure_ascii=False)}
Radar scores: {json.dumps(radar_scores, ensure_ascii=False)}"""
        return self._generate(prompt, self._fallback_persona(company_name, channel_data, radar_scores), 700)

    def generate_executive_verdict(self, all_data: List[Dict], scores: Dict, winner: str) -> str:
        fallback = f"{winner} is the intelligence winner because it leads the comparison on the weighted performance model. The market gap is the absence of a disciplined, recurring format system that combines high-search utility, strong audience interaction, and reliable publishing cadence. The primary company should treat the competitor set as proof that reach alone is not enough; the advantage will come from turning repeatable audience problems into ownable series. The next 90 days should prioritize SEO depth, tighter topic architecture, and formats that convert passive views into measurable engagement."
        prompt = f"""Write a 4-5 sentence executive verdict for a CMO. Declare the winner with confidence, cite specific data, identify the biggest market gap, and make the strategic implication clear.
Winner: {winner}
Companies: {json.dumps([self._compact_channel(company) for company in all_data], ensure_ascii=False)}
Scores: {json.dumps(scores, ensure_ascii=False)}"""
        return self._generate(prompt, fallback, 1000)

    def generate_steal_this_strategy(self, company_name: str, top_video: Dict, channel_data: Dict) -> List[str]:
        fallback = [
            f"Lead with the same audience trigger as \"{top_video.get('title', 'the top video')}\": a concrete promise, recognizable context, and low-friction payoff.",
            "Package the idea as a repeatable series so the channel can compound search behavior and returning-viewer memory.",
            "Use comments and retention signals from the winning format to decide the next three adjacent topics instead of treating the video as a one-off success.",
        ]
        prompt = f"""Return exactly 3 actionable bullet points as JSON array of strings. Explain why this top video worked, what principle it demonstrates, and how a competitor can replicate the principle without copying the creative.
Company: {company_name}
Top video: {json.dumps(top_video, ensure_ascii=False)}
Channel metrics: {json.dumps(self._compact_channel(channel_data), ensure_ascii=False)}"""
        text = self._generate(prompt, json.dumps(fallback), 900)
        return self._json_list(text, fallback)[:3]

    def generate_whitespace_analysis(self, all_data: List[Dict]) -> List[Dict]:
        fallback = [
            {"title": "Decision-Led Education Series", "description": "Competitors publish brand-first videos more often than buyer-problem explainers, leaving room for helpful category authority.", "format": "Weekly explainer series", "potential": "High"},
            {"title": "Short-Form Myth Breakdown", "description": "Common category misconceptions can be turned into fast recurring videos with strong search and sharing potential.", "format": "45-second vertical shorts", "potential": "High"},
            {"title": "Behind-the-Process Trust Content", "description": "Production, sourcing, quality, and safety stories are underused as trust-building assets.", "format": "Documentary micro-series", "potential": "Medium"},
            {"title": "Comparison and Use-Case Guides", "description": "Few channels own comparison-led content that helps viewers choose products for specific occasions.", "format": "Search-led guide videos", "potential": "High"},
        ]
        prompt = f"""Return valid JSON array with 4-5 objects. Each object must have title, description, format, potential. Identify topic or format gaps none of these competitors covers well.
Competitor data: {json.dumps([self._compact_channel(company) for company in all_data], ensure_ascii=False)}"""
        text = self._generate(prompt, json.dumps(fallback), 1200)
        return self._json_objects(text, fallback)

    def generate_90_day_plan(self, primary_company: str, all_analysis: Dict) -> Dict:
        fallback = {
            "month_1": {"title": "Foundation", "actions": ["Audit the top 20 videos against title intent, retention promise, and comment themes.", "Create three repeatable content pillars tied to search demand and brand advantage.", "Standardize descriptions with links, hashtags, chapters, and next-video pathways."]},
            "month_2": {"title": "Differentiation", "actions": ["Launch one educational series and one proof-led series with fixed weekly cadence.", "Use competitor whitespace to publish comparison, myth, and process content.", "Refresh thumbnails and titles around the strongest viewer problem statements."]},
            "month_3": {"title": "Amplification", "actions": ["Scale the highest-engagement format into shorts, community posts, and long-form follow-ups.", "Partner with credible creators or experts around the winning pillar.", "Review performance by view efficiency, engagement lift, and subscriber conversion."]},
        }
        prompt = f"""Return valid JSON with keys month_1, month_2, month_3. Each month has title and actions array with 3-4 specific actions. Month 1 is Foundation, Month 2 is Differentiation, Month 3 is Amplification. Reference the actual analysis findings.
Primary company: {primary_company}
Analysis: {json.dumps(all_analysis, ensure_ascii=False, default=str)[:14000]}"""
        text = self._generate(prompt, json.dumps(fallback), 1400)
        return self._json_object(text, fallback)

    def classify_content_pillars(self, videos: List[Dict]) -> Dict[str, int]:
        titles = [video.get("title", "") for video in videos[:50] if video.get("title")]
        fallback = {pillar: 0 for pillar in PILLARS}
        for title in titles:
            low = title.lower()
            if any(word in low for word in ["how", "tips", "guide", "recipe", "tutorial", "step"]):
                fallback["Tutorial/How-To"] += 1
            elif any(word in low for word in ["new", "launch", "product", "milk", "butter", "cheese", "cream"]):
                fallback["Product Showcase"] += 1
            elif any(word in low for word in ["story", "journey", "legacy"]):
                fallback["Storytelling"] += 1
            elif any(word in low for word in ["festival", "day", "trend", "season"]):
                fallback["Trend/Topical"] += 1
            elif any(word in low for word in ["customer", "testimonial", "review"]):
                fallback["Social Proof"] += 1
            else:
                fallback["Brand Culture"] += 1
        if not self.available or not titles:
            return fallback
        prompt = f"""Classify each title into one of these exact pillars: {PILLARS}. Return only a valid JSON object where keys are pillars and values are counts.
Titles: {json.dumps(titles, ensure_ascii=False)}"""
        text = self._generate(prompt, json.dumps(fallback), 900)
        result = self._json_object(text, fallback)
        return {pillar: int(result.get(pillar, 0)) for pillar in PILLARS}

    @staticmethod
    def _extract_json(text: str):
        match = re.search(r"(\{.*\}|\[.*\])", text or "", re.S)
        if not match:
            raise ValueError("No JSON found")
        return json.loads(match.group(1))

    def _json_list(self, text: str, fallback: List[str]) -> List[str]:
        try:
            data = self._extract_json(text)
            return [str(item) for item in data] if isinstance(data, list) else fallback
        except Exception:
            return fallback

    def _json_objects(self, text: str, fallback: List[Dict]) -> List[Dict]:
        try:
            data = self._extract_json(text)
            if not isinstance(data, list):
                return fallback
            cleaned = []
            for item in data:
                if isinstance(item, dict):
                    cleaned.append({
                        "title": str(item.get("title", "Untitled opportunity")),
                        "description": str(item.get("description", "")),
                        "format": str(item.get("format", "Video series")),
                        "potential": str(item.get("potential", "Medium")),
                    })
            return cleaned or fallback
        except Exception:
            return fallback

    def _json_object(self, text: str, fallback: Dict) -> Dict:
        try:
            data = self._extract_json(text)
            return data if isinstance(data, dict) else fallback
        except Exception:
            return fallback
