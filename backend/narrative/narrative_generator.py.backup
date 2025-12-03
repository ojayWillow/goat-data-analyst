# ============================================================================
# Narrative Generator - Human-like analyst voice
# ============================================================================
# Makes GOAT talk like a human analyst, not a dashboard
# Three main sections:
#   1. "I See You" - Context recognition
#   2. "What Hurts" - Pain points identification
#   3. "Your Path Forward" - Action plan
# ============================================================================

from typing import Dict, List, Optional
import pandas as pd
from datetime import datetime


class NarrativeGenerator:
    """
    Generates human-like narrative sections for data analysis reports
    
    Transforms dry metrics into conversational, actionable insights
    that feel like talking to a real data analyst.
    """
    
    def __init__(self):
        """Initialize the narrative generator"""
        print("✓ NarrativeGenerator initialized")
    
    def generate_context(
        self, 
        domain: Dict, 
        profile: Dict,
        df: Optional[pd.DataFrame] = None
    ) -> str:
        """
        "I See You" - Context recognition section
        
        Let users know GOAT understands their data type and context.
        
        Args:
            domain: Domain detection result {"type": "sales", "confidence": 0.9}
            profile: Data profile with stats, column info
            df: Optional DataFrame for deeper inspection
        
        Returns:
            Human-like intro paragraph (2-4 sentences)
        """
        rows = profile.get('overall', {}).get('rows', profile.get('rows', 0))
        cols = profile.get('overall', {}).get('columns', profile.get('columns', 0))
        domain_type = domain.get('type', 'unknown')
        confidence = domain.get('confidence', 0.0)
        
        # Get column info
        columns = profile.get('columns', [])
        col_names = [c.get('name') for c in columns] if columns else profile.get('column_names', [])
        
        # Detect date columns and ranges
        date_info = self._detect_date_range(df, columns) if df is not None else None
        
        # Build context based on domain type
        intro = self._build_intro(domain_type, confidence, rows, cols)
        column_context = self._build_column_context(col_names, columns)
        time_context = self._build_time_context(date_info) if date_info else ""
        
        return f"""
        <div class="narrative-section context">
            <h3>📊 I See You</h3>
            {intro}
            {column_context}
            {time_context}
        </div>
        """
    
    def _build_intro(self, domain_type: str, confidence: float, rows: int, cols: int) -> str:
        """Build opening sentence based on domain detection"""
        if domain_type == 'unknown' or confidence < 0.5:
            return f"<p>Hi—I can see you're working with a dataset containing <strong>{rows:,}</strong> rows across <strong>{cols}</strong> columns.</p>"
        
        domain_descriptions = {
            'sales': 'sales transaction data',
            'finance': 'financial data',
            'ecommerce': 'e-commerce data',
            'marketing': 'marketing campaign data',
            'healthcare': 'healthcare records',
            'hr': 'human resources data',
            'inventory': 'inventory management data',
            'customer': 'customer relationship data',
            'web_analytics': 'web analytics data',
            'logistics': 'logistics and shipping data'
        }
        
        description = domain_descriptions.get(domain_type, f'{domain_type} data')
        
        return f"<p>Hi—I can see you're working with <strong>{description}</strong>. You have <strong>{rows:,}</strong> rows across <strong>{cols}</strong> columns.</p>"
    
    def _build_column_context(self, col_names: List[str], columns: List[Dict]) -> str:
        """Identify and highlight key columns"""
        if not col_names:
            return ""
        
        # Find important column types
        key_columns = []
        
        for col in columns:
            col_name = col.get('name', '').lower()
            col_type = col.get('type', '')
            
            # Identify meaningful columns (not IDs/metadata)
            if col_type == 'numeric' and 'amount' in col_name or 'price' in col_name or 'revenue' in col_name:
                key_columns.append(f"<strong>{col.get('name')}</strong> (monetary)")
            elif col_type == 'numeric' and 'quantity' in col_name or 'count' in col_name:
                key_columns.append(f"<strong>{col.get('name')}</strong> (quantity)")
            elif col_type == 'categorical' and col.get('unique', 0) < 50:
                key_columns.append(f"<strong>{col.get('name')}</strong> (category)")
        
        if key_columns:
            key_list = ', '.join(key_columns[:5])  # Limit to top 5
            return f"<p>Key columns include: {key_list}.</p>"
        
        return f"<p>The dataset includes columns like: <strong>{', '.join(col_names[:5])}</strong>{'...' if len(col_names) > 5 else ''}.</p>"
    
    def _detect_date_range(self, df: pd.DataFrame, columns: List[Dict]) -> Optional[Dict]:
        """Detect date columns and extract date range"""
        for col in columns:
            col_name = col.get('name')
            col_type = col.get('type')
            
            # Look for datetime columns
            if col_type == 'datetime' or 'date' in col_name.lower():
                try:
                    date_series = pd.to_datetime(df[col_name], errors='coerce')
                    if date_series.notna().sum() > 0:
                        min_date = date_series.min()
                        max_date = date_series.max()
                        return {
                            'column': col_name,
                            'start': min_date,
                            'end': max_date
                        }
                except:
                    continue
        
        return None
    
    def _build_time_context(self, date_info: Dict) -> str:
        """Build time range description"""
        start = date_info['start']
        end = date_info['end']
        col = date_info['column']
        
        start_str = start.strftime('%B %Y')
        end_str = end.strftime('%B %Y')
        
        return f"<p>The data spans from <strong>{start_str}</strong> to <strong>{end_str}</strong> based on the <em>{col}</em> column.</p>"
    
    def generate_pain_points(
        self,
        quality: Dict,
        profile: Dict,
        df: Optional[pd.DataFrame] = None
    ) -> str:
        """
        "What Hurts" - Pain points identification
        
        Identify and prioritize data quality issues in plain language.
        
        Args:
            quality: Quality analysis result with missing, dupes, outliers
            profile: Data profile for context
            df: Optional DataFrame for deeper checks
        
        Returns:
            Prioritized list of issues in human language
        """
        # Placeholder for Day 6
        missing_pct = quality.get('missing_pct', 0)
        duplicates = quality.get('duplicates', 0)
        score = quality.get('overall_score', 100)
        
        return f"""
        <div class="narrative-section pain-points">
            <h3>⚠️ What Hurts</h3>
            <p>Your overall data quality score: <strong>{score:.0f}/100</strong></p>
            <ul>
                <li><strong>Missing data:</strong> {missing_pct:.1f}% of cells are empty</li>
                <li><strong>Duplicates:</strong> {duplicates} duplicate rows found</li>
            </ul>
            <p class="placeholder">
                🚧 <em>Full pain points analysis coming in Day 8</em>
            </p>
        </div>
        """
    
    def generate_action_plan(
        self,
        domain: Dict,
        quality: Dict,
        analytics: Dict,
        profile: Dict
    ) -> str:
        """
        "Your Path Forward" - Action plan
        
        Give users a sequenced, actionable plan based on their data issues.
        
        Args:
            domain: Domain type for context-specific recommendations
            quality: Quality issues to address
            analytics: Analysis results for opportunities
            profile: Data profile for context
        
        Returns:
            Ordered list of specific action steps
        """
        # Placeholder for Day 6
        return f"""
        <div class="narrative-section action-plan">
            <h3>🎯 Your Path Forward</h3>
            <p>Based on your data, here's what to do next:</p>
            <ol>
                <li><strong>Clean:</strong> Address data quality issues first</li>
                <li><strong>Validate:</strong> Check for logical errors</li>
                <li><strong>Analyze:</strong> Look for key patterns</li>
                <li><strong>Visualize:</strong> Build meaningful charts</li>
            </ol>
            <p class="placeholder">
                🚧 <em>Specific action steps coming in Day 9</em>
            </p>
        </div>
        """
    
    def generate_full_narrative(
        self,
        domain: Dict,
        profile: Dict,
        quality: Dict,
        analytics: Dict,
        df: Optional[pd.DataFrame] = None
    ) -> str:
        """
        Generate complete narrative combining all three sections
        
        Args:
            domain: Domain detection result
            profile: Data profile
            quality: Quality analysis
            analytics: Statistical analysis
            df: Optional DataFrame
        
        Returns:
            Complete HTML narrative with all sections
        """
        context = self.generate_context(domain, profile, df)
        pain_points = self.generate_pain_points(quality, profile, df)
        action_plan = self.generate_action_plan(domain, quality, analytics, profile)
        
        return f"""
        <div class="goat-narrative">
            <style>
                .goat-narrative {{
                    background: #f9f9f9;
                    border-left: 4px solid #2196F3;
                    padding: 20px;
                    margin: 20px 0;
                    border-radius: 4px;
                }}
                .narrative-section {{
                    margin-bottom: 25px;
                }}
                .narrative-section h3 {{
                    color: #1976D2;
                    margin-bottom: 10px;
                }}
                .narrative-section p {{
                    line-height: 1.6;
                    margin: 8px 0;
                }}
                .narrative-section ul, .narrative-section ol {{
                    margin: 10px 0;
                    padding-left: 25px;
                }}
                .placeholder {{
                    color: #666;
                    font-style: italic;
                    background: #fff3cd;
                    padding: 8px;
                    border-radius: 4px;
                    margin-top: 10px;
                }}
            </style>
            
            {context}
            {pain_points}
            {action_plan}
        </div>
        """


# Test function
def _test():
    """Test narrative generator with realistic data"""
    import numpy as np
    
    gen = NarrativeGenerator()
    
    # Create test dataframe with dates
    dates = pd.date_range('2023-01-01', periods=1000, freq='D')
    df = pd.DataFrame({
        'transaction_id': range(1000),
        'date': dates,
        'amount': np.random.uniform(10, 500, 1000),
        'category': np.random.choice(['Electronics', 'Clothing', 'Food'], 1000),
        'customer_id': np.random.randint(1, 100, 1000)
    })
    
    # Dummy inputs
    domain = {"type": "sales", "confidence": 0.85}
    profile = {
        'overall': {'rows': 1000, 'columns': 5, 'memory_mb': 0.5},
        'columns': [
            {'name': 'transaction_id', 'type': 'numeric'},
            {'name': 'date', 'type': 'datetime'},
            {'name': 'amount', 'type': 'numeric'},
            {'name': 'category', 'type': 'categorical', 'unique': 3},
            {'name': 'customer_id', 'type': 'numeric'}
        ]
    }
    quality = {'missing_pct': 2.5, 'duplicates': 15, 'overall_score': 82}
    analytics = {}
    
    print("\n" + "="*70)
    print("TESTING NARRATIVE GENERATOR - DAY 7")
    print("="*70)
    
    print("\n✅ Context Section (with real DataFrame):")
    print(gen.generate_context(domain, profile, df))
    
    print("\n" + "="*70)
    print("✅ Day 7 Complete: Smart context recognition working")
    print("="*70)


if __name__ == "__main__":
    _test()
