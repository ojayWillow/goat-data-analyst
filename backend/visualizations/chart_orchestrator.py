from typing import Dict, List, Type
import pandas as pd
from .base_chart import BaseChart
from .charts.timeseries_chart import TimeSeriesChart
from .charts.distribution_chart import DistributionChart
from .charts.correlation_chart import CorrelationChart
from .charts.category_chart import CategoryChart
from .profile_intelligence import ProfileIntelligence


class ChartOrchestrator:
    """
    Orchestrates chart generation using profile intelligence.
    Only generates relevant charts with meaningful data.
    """
    
    AVAILABLE_CHARTS: List[Type[BaseChart]] = [
        TimeSeriesChart,
        DistributionChart,
        CorrelationChart,
        CategoryChart
    ]
    
    def __init__(self, df: pd.DataFrame, domain: str = None, profile: dict = None):
        self.df = df
        self.domain = domain
        self.profile = profile or {}
        self.intelligence = ProfileIntelligence(df, self.profile)
    
    def generate_all_charts(self) -> Dict[str, str]:
        """
        Generate only relevant charts based on profile intelligence.
        Returns dict with chart_name -> HTML mapping.
        """
        charts = {}
        
        for ChartClass in self.AVAILABLE_CHARTS:
            chart = ChartClass(self.df, self.domain)
            
            # Check if this chart type should be generated
            if not self.intelligence.should_generate_chart(chart.chart_name):
                continue
            
            # Pass intelligence helper to chart
            if hasattr(chart, 'set_intelligence'):
                chart.set_intelligence(self.intelligence)
            
            # Only generate if chart is applicable
            if chart.can_generate():
                html = chart.generate()
                if html:
                    charts[chart.chart_name] = html
        
        return charts
    
    def generate_specific_charts(self, chart_names: List[str]) -> Dict[str, str]:
        """Generate only specific charts by name."""
        charts = {}
        
        for ChartClass in self.AVAILABLE_CHARTS:
            chart = ChartClass(self.df, self.domain)
            
            if chart.chart_name in chart_names:
                # Pass intelligence helper
                if hasattr(chart, 'set_intelligence'):
                    chart.set_intelligence(self.intelligence)
                
                if chart.can_generate():
                    html = chart.generate()
                    if html:
                        charts[chart.chart_name] = html
        
        return charts
