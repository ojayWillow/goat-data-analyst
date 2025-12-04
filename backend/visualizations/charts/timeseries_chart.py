import pandas as pd
import plotly.graph_objects as go
from ..base_chart import BaseChart


class TimeSeriesChart(BaseChart):
    """Generates time series visualization when date column exists."""
    
    def __init__(self, df, domain=None):
        super().__init__(df, domain)
        self.intelligence = None
    
    def set_intelligence(self, intelligence):
        """Receive profile intelligence helper."""
        self.intelligence = intelligence
    
    @property
    def chart_name(self) -> str:
        return "time_series"
    
    def can_generate(self) -> bool:
        """Check if dataframe has datetime columns."""
        if self.intelligence:
            return len(self.intelligence.get_datetime_columns()) > 0
        return False
    
    def generate(self) -> str:
        """Generate time series chart HTML."""
        if not self.can_generate():
            return ""
        
        # Get datetime column from intelligence
        date_cols = self.intelligence.get_datetime_columns()
        if not date_cols:
            return ""
        
        date_col = date_cols[0]
        
        # Sample if too large
        df_sample = self.df if len(self.df) <= 10000 else self.df.sample(10000)
        
        # Group by date and count
        time_data = df_sample[date_col].value_counts().sort_index()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=time_data.index,
            y=time_data.values,
            mode='lines+markers',
            name='Volume',
            line=dict(color='#10b981', width=2),
            marker=dict(size=4)
        ))
        
        fig.update_layout(
            title=f"Volume Over Time ({date_col})",
            xaxis_title=date_col,
            yaxis_title="Count",
            template="plotly_white",
            hovermode='x unified',
            height=400,
            margin=dict(l=50, r=50, t=50, b=50)
        )
        
        return fig.to_html(include_plotlyjs=False, full_html=False, div_id=f"chart-{self.chart_name}")
