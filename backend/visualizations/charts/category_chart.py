import pandas as pd
import plotly.graph_objects as go
from ..base_chart import BaseChart


class CategoryChart(BaseChart):
    """Generates category breakdown bar chart."""
    
    def __init__(self, df, domain=None):
        super().__init__(df, domain)
        self.intelligence = None
    
    def set_intelligence(self, intelligence):
        """Receive profile intelligence helper."""
        self.intelligence = intelligence
    
    @property
    def chart_name(self) -> str:
        return "category"
    
    def can_generate(self) -> bool:
        """Check if we have meaningful categorical columns."""
        if self.intelligence:
            return len(self.intelligence.get_key_categorical_columns(max_cols=1)) > 0
        return False
    
    def generate(self) -> str:
        """Generate category breakdown chart HTML."""
        if not self.can_generate():
            return ""
        
        # Get best categorical column from intelligence
        key_cols = self.intelligence.get_key_categorical_columns(max_cols=1)
        if not key_cols:
            return ""
        
        cat_col = key_cols[0]
        
        # Get top 10 categories
        category_counts = self.df[cat_col].value_counts().head(10)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=category_counts.index,
            y=category_counts.values,
            marker_color='#8b5cf6',
            name=cat_col
        ))
        
        fig.update_layout(
            title=f"Top Categories in {cat_col}",
            xaxis_title=cat_col,
            yaxis_title="Count",
            template="plotly_white",
            showlegend=False,
            height=400,
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        return fig.to_html(include_plotlyjs=False, full_html=False, div_id=f"chart-{self.chart_name}")
