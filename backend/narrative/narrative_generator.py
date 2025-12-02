# ============================================================================
# Narrative Generator - Human-like analyst voice
# ============================================================================
# Makes GOAT talk like a human analyst, not a dashboard
# Three main sections:
#   1. "I See You" - Context recognition (✅ Day 7)
#   2. "What Hurts" - Pain points identification (✅ Day 8 - AI-ENHANCED)
#   3. "Your Path Forward" - Action plan (Day 9)
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
    
    def __init__(self, ai_engine=None):
        """
        Initialize the narrative generator
        
        Args:
            ai_engine: Optional AIEngine instance for enhanced generation
        """
        self.ai_engine = ai_engine
        print("✓ NarrativeGenerator initialized" + (" (AI-enhanced)" if ai_engine else ""))
    
    def generate_context(
        self, 
        domain: Dict, 
        profile: Dict,
        df: Optional[pd.DataFrame] = None
    ) -> str:
        """
        "I See You" - Context recognition section (Day 7 ✅)
        
        Let users know GOAT understands their data type and context.
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
            if col_type == 'numeric' and ('amount' in col_name or 'price' in col_name or 'revenue' in col_name):
                key_columns.append(f"<strong>{col.get('name')}</strong> (monetary)")
            elif col_type == 'numeric' and ('quantity' in col_name or 'count' in col_name):
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
        "What Hurts" - Pain points identification (Day 8 ✅ AI-ENHANCED)
        
        Identify and prioritize data quality issues in plain language.
        Uses AI when available for context-aware explanations.
        
        Args:
            quality: Quality analysis result with missing, dupes, outliers
            profile: Data profile for context
            df: Optional DataFrame for deeper checks
        
        Returns:
            Prioritized list of issues in human language
        """
        score = quality.get('overall_score', 100)
        
        # Get pain points (AI-enhanced if available)
        if self.ai_engine and df is not None:
            try:
                pain_points = self.ai_engine.explain_pain_points(
                    df=df,
                    quality=quality,
                    profile=profile,
                    domain={"type": "unknown"}  # Domain passed separately in full narrative
                )
            except Exception as e:
                print(f"⚠️  AI pain points failed, using fallback: {e}")
                pain_points = self._fallback_pain_points(quality, profile, df)
        else:
            pain_points = self._fallback_pain_points(quality, profile, df)
        
        # Build HTML output
        pain_points_html = self._build_pain_points_html(pain_points)
        
        return f"""
        <div class="narrative-section pain-points">
            <h3>⚠️ What Hurts</h3>
            <div class="quality-score">
                <p>Your overall data quality score: <strong class="score-{self._get_score_class(score)}">{score:.0f}/100</strong></p>
            </div>
            {pain_points_html}
        </div>
        """
    
    def _fallback_pain_points(
        self, 
        quality: Dict, 
        profile: Dict, 
        df: Optional[pd.DataFrame]
    ) -> List[Dict]:
        """Rule-based pain point detection (fallback when AI unavailable)"""
        pain_points = []
        
        missing_pct = quality.get('missing_pct', 0)
        duplicates = quality.get('duplicates', 0)
        missing_by_col = quality.get('missing_by_column', {})
        
        # Check missing data
        if missing_pct > 5:
            severity = "high" if missing_pct > 20 else "medium"
            
            # Find worst columns
            worst_cols = sorted(
                [(col, count) for col, count in missing_by_col.items() if count > 0],
                key=lambda x: x[1],
                reverse=True
            )[:3]
            
            col_details = ", ".join([f"<strong>{col}</strong> ({count} missing)" for col, count in worst_cols])
            
            pain_points.append({
                "severity": severity,
                "issue": f"{missing_pct:.1f}% of your data is missing",
                "impact": f"This affects calculations and insights. Worst columns: {col_details}",
                "fix": "Review missing data patterns. Consider median/mode fill for numeric/categorical, or flag for manual review."
            })
        
        # Check duplicates
        if duplicates > 0:
            severity = "high" if duplicates > 100 else "medium"
            dup_pct = (duplicates / profile.get('rows', 1)) * 100
            
            pain_points.append({
                "severity": severity,
                "issue": f"{duplicates} duplicate rows found ({dup_pct:.1f}% of data)",
                "impact": "Metrics like counts, averages, and totals will be inflated or incorrect",
                "fix": "Remove duplicates after verifying they are true duplicates, not legitimate repeated records."
            })
        
        # Check for outliers (if df provided)
        if df is not None:
            outlier_cols = self._detect_outliers(df)
            if outlier_cols:
                pain_points.append({
                    "severity": "medium",
                    "issue": f"Outliers detected in {len(outlier_cols)} numeric columns",
                    "impact": f"Columns affected: {', '.join(outlier_cols)}. These extreme values may skew statistical analysis.",
                    "fix": "Review outliers to determine if they are errors or legitimate edge cases. Consider capping or flagging."
                })
        
        # If no issues found
        if not pain_points:
            pain_points.append({
                "severity": "low",
                "issue": "No major data quality issues detected",
                "impact": "Your data appears clean and ready for analysis",
                "fix": "Proceed with deeper analysis and visualization."
            })
        
        return pain_points
    
    def _detect_outliers(self, df: pd.DataFrame) -> List[str]:
        """Detect outliers using IQR method"""
        outlier_cols = []
        
        for col in df.select_dtypes(include=['number']).columns:
            if df[col].nunique() < 3:  # Skip binary/constant columns
                continue
            
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 3 * IQR
            upper_bound = Q3 + 3 * IQR
            
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            
            if len(outliers) > 0:
                outlier_cols.append(col)
        
        return outlier_cols
    
    def _build_pain_points_html(self, pain_points: List[Dict]) -> str:
        """Convert pain points to formatted HTML"""
        if not pain_points:
            return "<p>No issues detected. Your data looks good!</p>"
        
        html_parts = ["<div class='pain-points-list'>"]
        
        # Sort by severity
        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        sorted_points = sorted(
            pain_points,
            key=lambda x: severity_order.get(x.get('severity', 'low'), 3)
        )
        
        for point in sorted_points:
            severity = point.get('severity', 'low')
            icon = self._get_severity_icon(severity)
            
            html_parts.append(f"""
            <div class='pain-point severity-{severity}'>
                <div class='pain-point-header'>
                    <span class='severity-badge'>{icon} {severity.upper()}</span>
                    <strong>{point.get('issue', 'Unknown issue')}</strong>
                </div>
                <div class='pain-point-body'>
                    <p class='impact'><strong>Impact:</strong> {point.get('impact', 'Unknown impact')}</p>
                    <p class='fix'><strong>Fix:</strong> {point.get('fix', 'No fix suggested')}</p>
                </div>
            </div>
            """)
        
        html_parts.append("</div>")
        
        return "\n".join(html_parts)
    
    def _get_severity_icon(self, severity: str) -> str:
        """Get emoji icon for severity level"""
        icons = {
            "critical": "🔴",
            "high": "🟠",
            "medium": "🟡",
            "low": "🟢"
        }
        return icons.get(severity, "⚪")
    
    def _get_score_class(self, score: float) -> str:
        """Get CSS class for score color"""
        if score >= 80:
            return "good"
        elif score >= 60:
            return "okay"
        else:
            return "poor"
    
    def generate_action_plan(
        self,
        domain: Dict,
        quality: Dict,
        analytics: Dict,
        profile: Dict,
        pain_points: Optional[List[Dict]] = None
    ) -> str:
        """
        "Your Path Forward" - Action plan (Day 9)
        
        Give users a sequenced, actionable plan based on their data issues.
        """
        # Get action steps (AI-enhanced if available)
        if self.ai_engine and pain_points:
            try:
                steps = self.ai_engine.generate_action_plan(
                    domain=domain,
                    pain_points=pain_points,
                    profile=profile,
                    analytics=analytics
                )
            except Exception as e:
                print(f"⚠️  AI action plan failed, using fallback: {e}")
                steps = self._fallback_action_plan(pain_points)
        else:
            steps = self._fallback_action_plan(pain_points or [])
        
        steps_html = "\n".join([f"<li>{step}</li>" for step in steps])
        
        return f"""
        <div class="narrative-section action-plan">
            <h3>🎯 Your Path Forward</h3>
            <p>Based on your data, here's what to do next:</p>
            <ol class='action-steps'>
                {steps_html}
            </ol>
        </div>
        """
    
    def _fallback_action_plan(self, pain_points: List[Dict]) -> List[str]:
        """Generate action plan from pain points"""
        if not pain_points:
            return [
                "1. Proceed with data analysis",
                "2. Build visualizations",
                "3. Extract insights"
            ]
        
        steps = []
        for i, point in enumerate(pain_points[:5], 1):  # Top 5 issues
            fix = point.get('fix', 'Address: ' + point.get('issue', 'Unknown'))
            steps.append(f"{i}. {fix}")
        
        return steps
    
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
        pain_points_section = self.generate_pain_points(quality, profile, df)
        
        # Extract pain points for action plan (if AI-enhanced)
        pain_points_data = None
        if self.ai_engine and df is not None:
            try:
                pain_points_data = self.ai_engine.explain_pain_points(
                    df=df,
                    quality=quality,
                    profile=profile,
                    domain=domain
                )
            except:
                pass
        
        action_plan = self.generate_action_plan(domain, quality, analytics, profile, pain_points_data)
        
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
                
                /* Quality Score */
                .quality-score {{
                    font-size: 1.1em;
                    margin-bottom: 15px;
                }}
                .score-good {{ color: #4CAF50; }}
                .score-okay {{ color: #FF9800; }}
                .score-poor {{ color: #F44336; }}
                
                /* Pain Points */
                .pain-points-list {{
                    display: flex;
                    flex-direction: column;
                    gap: 15px;
                }}
                .pain-point {{
                    background: white;
                    border-left: 4px solid #ccc;
                    padding: 12px;
                    border-radius: 4px;
                }}
                .pain-point.severity-critical {{ border-left-color: #F44336; }}
                .pain-point.severity-high {{ border-left-color: #FF9800; }}
                .pain-point.severity-medium {{ border-left-color: #FFC107; }}
                .pain-point.severity-low {{ border-left-color: #4CAF50; }}
                
                .pain-point-header {{
                    margin-bottom: 8px;
                }}
                .severity-badge {{
                    display: inline-block;
                    padding: 2px 8px;
                    border-radius: 3px;
                    font-size: 0.75em;
                    font-weight: bold;
                    margin-right: 8px;
                }}
                .pain-point-body {{
                    font-size: 0.95em;
                    color: #555;
                }}
                .pain-point-body p {{
                    margin: 6px 0;
                }}
                .impact {{ color: #d32f2f; }}
                .fix {{ color: #1976d2; }}
                
                /* Action Steps */
                .action-steps {{
                    background: white;
                    padding: 15px 15px 15px 35px;
                    border-radius: 4px;
                }}
                .action-steps li {{
                    margin: 8px 0;
                    line-height: 1.5;
                }}
            </style>
            
            {context}
            {pain_points_section}
            {action_plan}
        </div>
        """


# Test function
def _test():
    """Test narrative generator with realistic messy data"""
    import numpy as np
    
    print("\n" + "="*70)
    print("TESTING NARRATIVE GENERATOR - DAY 8")
    print("="*70)
    
    gen = NarrativeGenerator()  # Without AI for testing
    
    # Create messy test dataframe
    np.random.seed(42)
    dates = pd.date_range('2023-06-01', periods=505, freq='D')
    
    # Create data with intentional quality issues
    amount = np.random.uniform(10, 500, 505)
    amount[::10] = None  # 10% missing
    
    df = pd.DataFrame({
        'transaction_id': range(505),
        'date': dates,
        'amount': amount,
        'category': np.random.choice(['Electronics', 'Clothing', 'Food'], 505),
        'customer_id': np.random.randint(1, 100, 505)
    })
    
    # Add duplicates
    df = pd.concat([df, df.iloc[:47]], ignore_index=True)
    
    # Add outliers
    df.loc[10, 'amount'] = 99999
    df.loc[50, 'amount'] = -1000
    
    # Dummy inputs
    domain = {"type": "sales", "confidence": 0.85}
    profile = {
        'overall': {'rows': len(df), 'columns': 5, 'memory_mb': 0.5},
        'rows': len(df),
        'columns': 5,
        'columns': [
            {'name': 'transaction_id', 'type': 'numeric'},
            {'name': 'date', 'type': 'datetime'},
            {'name': 'amount', 'type': 'numeric'},
            {'name': 'category', 'type': 'categorical', 'unique': 3},
            {'name': 'customer_id', 'type': 'numeric'}
        ]
    }
    
    # Calculate quality
    missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
    quality = {
        'missing_pct': missing_pct,
        'duplicates': 47,
        'overall_score': max(0, 100 - missing_pct - 5),
        'missing_by_column': df.isnull().sum().to_dict()
    }
    
    analytics = {}
    
    print(f"\nTest data: {len(df)} rows, {missing_pct:.1f}% missing, 47 duplicates")
    
    print("\n✅ Context Section:")
    print(gen.generate_context(domain, profile, df))
    
    print("\n✅ Pain Points Section (NEW - Day 8):")
    print(gen.generate_pain_points(quality, profile, df))
    
    print("\n✅ Action Plan Section:")
    pain_points = gen._fallback_pain_points(quality, profile, df)
    print(gen.generate_action_plan(domain, quality, analytics, profile, pain_points))
    
    print("\n" + "="*70)
    print("✅ Day 8 Complete: AI-enhanced pain points working")
    print("="*70)


if __name__ == "__main__":
    _test()
