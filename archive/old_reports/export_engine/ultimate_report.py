import pandas as pd
from backend.export_engine.quality_report import QualityReportGenerator
from backend.visualizations.chart_orchestrator import ChartOrchestrator
from backend.reports.assembler import ReportAssembler


class UltimateReportGenerator:
    """
    The Grand Unifier - Orchestrates analysis and uses ReportAssembler 
    to generate the final HTML.
    """
    
    def __init__(self):
        """Initialize the report generator."""
        self.assembler = ReportAssembler()
        
        # Keep data containers for state
        self.df = None
        self.profile = None
        self.domain_result = None
        self.analytics = None
        self.ai_insights = None
        self.charts = {}
    
    def generate_report(
        self,
        df: pd.DataFrame,
        profile: dict,
        domain_result: dict = None,
        analytics: dict = None,
        ai_insights: dict = None,
        charts: dict = None,
        include_charts: bool = True
    ) -> str:
        """
        Generate the ultimate analysis report.
        """
        self.df = df
        self.profile = profile
        self.domain_result = domain_result
        self.analytics = analytics
        self.ai_insights = ai_insights
        self.charts = charts if charts else {}
        
        # 1. Use provided charts (don't regenerate)
        charts_data = {}
        if include_charts and charts:
            charts_data = charts
        
        # 2. Prepare AI Data
        insights_data = None
        if ai_insights:
            insights_data = {
                "insights": ai_insights.get("insights", []),
                "model": "Groq Llama 3",
                "timestamp": ""
            }
        
        # 3. Delegate HTML Generation to Assembler
        html = self.assembler.generate_report(
            profile=profile,
            domain_data=domain_result,
            insights_data=insights_data,
            charts_data=charts_data,
            config={
                "include_header": True,
                "include_quality": True,
                "include_domain": True if domain_result else False,
                "include_ai": True if insights_data else False,
                "include_charts": include_charts,
                "include_footer": True
            }
        )
        
        return html
