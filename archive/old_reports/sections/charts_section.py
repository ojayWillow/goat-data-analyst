"""Charts Section - Generates HTML for data visualizations."""

from typing import Dict, Any, Optional


class ChartsSection:
    """Generates charts HTML section."""

    def generate(self, charts_data: Dict[str, Any]) -> str:
        """
        Generate charts HTML.

        Args:
            charts_data: Dict containing:
                - time_series: str (HTML of time series chart) - optional
                - category: str (HTML of category chart) - optional
                - distribution: str (HTML of distribution chart) - optional
                - correlation: str (HTML of correlation heatmap) - optional

        Returns:
            HTML string for charts section
        """
        if not charts_data:
            return ""

        # Filter out empty charts
        charts = {k: v for k, v in charts_data.items() if v}

        if not charts:
            return ""

        html = """
        <div class="card">
            <div class="card-header">
                <h2>📈 Visualizations</h2>
            </div>
            <div class="card-body">
        """

        # Add each chart
        chart_titles = {
            "time_series": "Time Series Trends",
            "category": "Top Values",
            "distribution": "Distribution Analysis",
            "correlation": "Correlation Heatmap"
        }

        for chart_key, chart_html in charts.items():
            title = chart_titles.get(chart_key, chart_key.replace("_", " ").title())

            html += f"""
                <div style="margin-bottom: 24px;">
                    <h3 style="font-size: 1rem; margin-bottom: 12px;">📊 {title}</h3>
                    <div style="width: 100%; min-height: 400px;">
                        {chart_html}
                    </div>
                </div>
            """

        html += """
            </div>
        </div>
        """

        return html
