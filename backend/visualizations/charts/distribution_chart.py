import pandas as pd
import plotly.graph_objects as go
from ..base_chart import BaseChart


class DistributionChart(BaseChart):
    """Generates distribution histogram for numeric columns."""
    
    def __init__(self, df, domain=None):
        super().__init__(df, domain)
        self.intelligence = None
    
    def set_intelligence(self, intelligence):
        """Receive profile intelligence helper."""
        self.intelligence = intelligence
    
    @property
    def chart_name(self) -> str:
        return "distribution"
    
    def can_generate(self) -> bool:
        """Check if we have meaningful numeric columns."""
        if self.intelligence:
            return len(self.intelligence.get_key_numeric_columns(max_cols=1)) > 0
        return False
    
    def generate(self) -> str:
        """Generate distribution chart HTML."""
        if not self.can_generate():
            return ""
        
        # Get best numeric column from intelligence
        key_cols = self.intelligence.get_key_numeric_columns(max_cols=1)
        if not key_cols:
            return ""
        
        numeric_col = key_cols[0]
        
        # Sample if too large
        df_sample = self.df if len(self.df) <= 10000 else self.df.sample(10000)
        
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=df_sample[numeric_col],
            marker_color='#3b82f6',
            name=numeric_col,
            nbinsx=30
        ))
        
        fig.update_layout(
            title=f"Distribution of {numeric_col}",
            xaxis_title=numeric_col,
            yaxis_title="Frequency",
            template="plotly_white",
            showlegend=False,
            height=400,
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        return fig.to_html(include_plotlyjs=False, div_id=f"chart-{self.chart_name}")
