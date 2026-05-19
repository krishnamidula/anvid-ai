import base64
from io import BytesIO
from typing import Dict, List

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


class ChartGenerator:
    BG = "#0F1117"
    CARD = "#1E2130"
    TEXT = "#FFFFFF"
    MUTED = "#A0A0B0"
    GRID = "#2D3250"
    COLORS = ["#6C63FF", "#43B89C", "#FF6584", "#FFB347", "#A78BFA"]

    def __init__(self):
        sns.set_theme(style="darkgrid")

    def _finish(self) -> str:
        buffer = BytesIO()
        plt.tight_layout()
        plt.savefig(buffer, format="png", dpi=180, facecolor=self.BG, bbox_inches="tight")
        plt.close()
        buffer.seek(0)
        return base64.b64encode(buffer.read()).decode("utf-8")

    def generate_radar_chart(self, all_radar_scores: Dict) -> str:
        dimensions = ["consistency", "engagement", "audience_growth", "content_performance", "activity_level", "overall_strength"]
        labels = ["Consistency", "Engagement", "Growth", "Performance", "Activity", "Strength"]
        angles = np.linspace(0, 2 * np.pi, len(dimensions), endpoint=False).tolist()
        angles += angles[:1]
        plt.figure(figsize=(9.2, 5.4), facecolor=self.BG)
        ax = plt.subplot(111, polar=True, facecolor=self.BG)
        for index, (company, scores) in enumerate(all_radar_scores.items()):
            values = [scores.get(dimension, 0) for dimension in dimensions]
            values += values[:1]
            color = self.COLORS[index % len(self.COLORS)]
            ax.plot(angles, values, color=color, linewidth=2.2, label=company)
            ax.fill(angles, values, color=color, alpha=0.2)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels, color=self.TEXT, fontsize=9)
        ax.set_ylim(0, 100)
        ax.tick_params(colors=self.MUTED)
        ax.grid(color=self.GRID, alpha=0.8)
        ax.spines["polar"].set_color(self.GRID)
        ax.legend(loc="upper right", bbox_to_anchor=(1.28, 1.15), facecolor=self.CARD, edgecolor=self.GRID, labelcolor=self.TEXT)
        return self._finish()

    def generate_engagement_scatter(self, all_channel_data: List[Dict]) -> str:
        valid = [company for company in all_channel_data if not company.get("error")]
        plt.figure(figsize=(8.4, 5.2), facecolor=self.BG)
        ax = plt.gca()
        ax.set_facecolor(self.BG)
        for index, company in enumerate(valid):
            size = max(90, min(900, np.sqrt(company.get("subscribers", 0) or 1) / 18))
            ax.scatter(company.get("avg_views", 0), company.get("avg_engagement_rate", 0), s=size, color=self.COLORS[index % len(self.COLORS)], alpha=0.82, edgecolors="white", linewidth=0.7)
            ax.text(company.get("avg_views", 0), company.get("avg_engagement_rate", 0), company["name"], color=self.TEXT, fontsize=8, ha="center", va="bottom")
        if valid:
            x_mid = float(np.mean([company.get("avg_views", 0) for company in valid]))
            y_mid = float(np.mean([company.get("avg_engagement_rate", 0) for company in valid]))
            ax.axvline(x_mid, color=self.GRID, linestyle="--", linewidth=1)
            ax.axhline(y_mid, color=self.GRID, linestyle="--", linewidth=1)
            ax.text(0.82, 0.88, "Stars", transform=ax.transAxes, color=self.MUTED, fontsize=9)
            ax.text(0.08, 0.88, "Hidden Gems", transform=ax.transAxes, color=self.MUTED, fontsize=9)
            ax.text(0.72, 0.12, "Scale Without Depth", transform=ax.transAxes, color=self.MUTED, fontsize=9)
            ax.text(0.07, 0.12, "Under-Leveraged", transform=ax.transAxes, color=self.MUTED, fontsize=9)
        ax.set_xlabel("Average Views", color=self.TEXT)
        ax.set_ylabel("Engagement Rate", color=self.TEXT)
        ax.tick_params(colors=self.MUTED)
        ax.grid(color=self.GRID, alpha=0.65)
        for spine in ax.spines.values():
            spine.set_color(self.GRID)
        return self._finish()

    def generate_content_pillar_chart(self, all_pillar_data: Dict) -> str:
        data = pd.DataFrame(all_pillar_data).fillna(0).T
        if data.empty:
            data = pd.DataFrame({"Brand Culture": [1]}, index=["No data"])
        percentages = data.div(data.sum(axis=1).replace(0, 1), axis=0) * 100
        plt.figure(figsize=(9.4, 5.2), facecolor=self.BG)
        ax = plt.gca()
        ax.set_facecolor(self.BG)
        left = np.zeros(len(percentages))
        for index, column in enumerate(percentages.columns):
            values = percentages[column].values
            ax.barh(percentages.index, values, left=left, label=column, color=self.COLORS[index % len(self.COLORS)])
            for row_index, value in enumerate(values):
                if value >= 9:
                    ax.text(left[row_index] + value / 2, row_index, f"{value:.0f}%", va="center", ha="center", color=self.TEXT, fontsize=7)
            left += values
        ax.set_xlim(0, 100)
        ax.tick_params(colors=self.MUTED)
        ax.grid(axis="x", color=self.GRID, alpha=0.6)
        ax.legend(fontsize=7, facecolor=self.CARD, edgecolor=self.GRID, labelcolor=self.TEXT, loc="lower center", bbox_to_anchor=(0.5, -0.32), ncol=3)
        for spine in ax.spines.values():
            spine.set_color(self.GRID)
        return self._finish()

    def generate_cadence_chart(self, all_upload_dates: Dict) -> str:
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        rows = max(1, len(all_upload_dates))
        fig, axes = plt.subplots(rows, 1, figsize=(9.2, max(3.0, rows * 1.45)), facecolor=self.BG)
        if rows == 1:
            axes = [axes]
        for index, (company, distribution) in enumerate(all_upload_dates.items()):
            ax = axes[index]
            ax.set_facecolor(self.BG)
            ax.bar(days, [distribution.get(day, 0) for day in days], color=self.COLORS[index % len(self.COLORS)])
            ax.set_title(company, color=self.TEXT, loc="left", fontsize=10, pad=6)
            ax.tick_params(colors=self.MUTED, labelsize=8)
            ax.grid(axis="y", color=self.GRID, alpha=0.55)
            for spine in ax.spines.values():
                spine.set_color(self.GRID)
        return self._finish()
