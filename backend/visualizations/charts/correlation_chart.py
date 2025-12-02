import pandas as pd
import plotly.graph_objects as go
from ..base_chart import BaseChart


class CorrelationChart(BaseChart):
    """Generates correlation heatmap for numeric columns."""
    
    def __init__(self, df, domain=None):
        super().__init__(df, domain)
        self.intelligence = None
    
    def set_intelligence(self, intelligence):
        """Receive profile intelligence helper."""
        self.intelligence = intelligence
    
    @property
    def chart_name(self) -> str:
        return "correlation"
    
    def can_generate(self) -> bool:
        """Check if we have at least 2 meaningful numeric columns."""
        if self.intelligence:
            return len(self.intelligence.get_key_numeric_columns(max_cols=10)) >= 2
        return False
    
    def generate(self) -> str:
        """Generate correlation heatmap HTML."""
        if not self.can_generate():
            return ""
        
        # Get meaningful numeric columns from intelligence
        key_cols = self.intelligence.get_key_numeric_columns(max_cols=15)
        if len(key_cols) < 2:
            return ""
        
        numeric_df = self.df[key_cols]
        
        # Sample if too large
        if len(numeric_df) > 5000:
            numeric_df = numeric_df.sample(5000)
        
        # Calculate correlation matrix
        corr_matrix = numeric_df.corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            text=corr_matrix.values.round(2),
            texttemplate='%{text}',
            textfont={"size": 10},
            colorbar=dict(title="Correlation")
        ))
        
        fig.update_layout(
            title="Correlation Matrix",
            template="plotly_white",
            height=800,
            width=1100,
            margin=dict(l=150, r=50, t=80, b=150)
        )
        
        return fig.to_html(include_plotlyjs=False, div_id=f"chart-{self.chart_name}")
