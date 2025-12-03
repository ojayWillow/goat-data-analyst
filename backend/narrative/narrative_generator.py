# ============================================================================
# Narrative Generator - Human-like analyst voice
# ============================================================================
# Makes GOAT talk like a human analyst, not a dashboard
# Three main sections:
#   1. "I See You" - Context recognition (✅ Day 7)
#   2. "What Hurts" - Pain points identification (✅ Day 8 - AI-ENHANCED)
#   3. "Your Path Forward" - Action plan (✅ Day 9 - DOMAIN-AWARE)
#   4. Fix Suggestions - Actionable fixes (✅ Day 12 - NEW)
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
    
    # ========================================================================
    # DAY 7: "I See You" - Context Recognition
    # ========================================================================
    
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
    
    # ========================================================================
    # DAY 8: "What Hurts" - Pain Points Analysis
    # ========================================================================
    
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
        """
        score = quality.get('overall_score', 100)
        
        # Get pain points (AI-enhanced if available)
        if self.ai_engine and self.ai_engine.enabled and df is not None:
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
        
        # 1. Check missing data
        if missing_pct > 5:
            severity = "high" if missing_pct > 20 else "medium"
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
        
        # 2. Check duplicates
        if duplicates > 0:
            severity = "high" if duplicates > 100 else "medium"
            dup_pct = (duplicates / profile.get('rows', 1)) * 100
            
            pain_points.append({
                "severity": severity,
                "issue": f"{duplicates} duplicate rows found ({dup_pct:.1f}% of data)",
                "impact": "Metrics like counts, averages, and totals will be inflated or incorrect",
                "fix": "Remove duplicates after verifying they are true duplicates, not legitimate repeated records."
            })
        
        # 3. Check for outliers
        outliers = quality.get('outliers', {})
        if outliers:
            outlier_cols = list(outliers.keys())
            outlier_details = ', '.join([f"<strong>{col}</strong> ({outliers[col]['count']})" for col in outlier_cols[:3]])
            
            pain_points.append({
                "severity": "medium",
                "issue": f"Outliers detected in {len(outliers)} numeric columns",
                "impact": f"Columns affected: {outlier_details}. These extreme values may skew statistical analysis.",
                "fix": "Review outliers to determine if they are errors or legitimate edge cases. Consider capping or flagging."
            })
        
        # 4. Check for date format issues
        date_issues = quality.get('date_format_issues', {})
        if date_issues:
            date_cols = ', '.join([f"<strong>{col}</strong>" for col in list(date_issues.keys())[:3]])
            
            pain_points.append({
                "severity": "medium",
                "issue": f"Inconsistent date formats in {len(date_issues)} columns",
                "impact": f"Affected columns: {date_cols}. Date parsing and time-based analysis may fail.",
                "fix": "Standardize all dates to a single format (e.g., YYYY-MM-DD)."
            })
        
        # 5. Check for capitalization issues
        cap_issues = quality.get('capitalization_issues', {})
        if cap_issues:
            cap_cols = ', '.join([f"<strong>{col}</strong>" for col in list(cap_issues.keys())[:3]])
            
            pain_points.append({
                "severity": "low",
                "issue": f"Inconsistent capitalization in {len(cap_issues)} columns",
                "impact": f"Affected columns: {cap_cols}. Grouping and counting will produce incorrect results.",
                "fix": "Standardize text to lowercase or title case for consistency."
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
    
    # ========================================================================
    # DAY 9: "Your Path Forward" - Action Plan (DOMAIN-AWARE)
    # ========================================================================
    
    def generate_action_plan(
        self,
        domain: Dict,
        quality: Dict,
        analytics: Dict,
        profile: Dict
    ) -> str:
        """
        "Your Path Forward" - Action plan (Day 9 ✅ ENHANCED)
        
        Give users a sequenced, actionable plan based on their data issues.
        Now with domain-aware recommendations and smart sequencing.
        """
        # Extract pain points from quality metrics
        pain_points = self._extract_pain_points_from_quality(quality, profile)
        
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
                print(f"⚠️  AI action plan failed, using enhanced fallback: {e}")
                steps = self._enhanced_action_plan(domain, quality, profile, pain_points)
        else:
            # Use enhanced fallback with domain awareness
            steps = self._enhanced_action_plan(domain, quality, profile, pain_points)
        
        # Get intro based on severity
        intro = self._get_action_intro(pain_points)
        
        steps_html = "\n".join([f"<li>{step}</li>" for step in steps])
        
        return f"""
        <div class="narrative-section action-plan">
            <h3>🎯 Your Path Forward</h3>
            <p>{intro}</p>
            <ol class='action-steps'>
                {steps_html}
            </ol>
        </div>
        """
    
    def _extract_pain_points_from_quality(self, quality: Dict, profile: Dict) -> List[Dict]:
        """Extract pain points from quality metrics"""
        pain_points = []
        
        missing_pct = quality.get('missing_pct', 0)
        duplicates = quality.get('duplicates', 0)
        
        if missing_pct > 5:
            severity = "high" if missing_pct > 20 else "medium"
            pain_points.append({
                "severity": severity,
                "issue": f"{missing_pct:.1f}% missing data",
                "fix": f"Fill or flag {missing_pct:.1f}% missing values"
            })
        
        if duplicates > 0:
            severity = "high" if duplicates > 100 else "medium"
            pain_points.append({
                "severity": severity,
                "issue": f"{duplicates} duplicate rows",
                "fix": f"Remove {duplicates} duplicate rows after verification"
            })
        
        return pain_points
    
    def _get_action_intro(self, pain_points: List[Dict]) -> str:
        """Get contextual intro based on pain severity"""
        if not pain_points:
            return "Your data looks clean! Here's how to get the most value from it:"
        
        high_severity = sum(1 for p in pain_points if p.get('severity') in ['critical', 'high'])
        
        if high_severity >= 3:
            return "⚠️ <strong>Your data needs immediate attention.</strong> Follow these steps in order:"
        elif high_severity > 0:
            return "Here's a prioritized plan to address your data quality issues:"
        else:
            return "Your data quality is good overall. Here are recommended improvements:"
    
    def _enhanced_action_plan(
        self,
        domain: Dict,
        quality: Dict,
        profile: Dict,
        pain_points: List[Dict]
    ) -> List[str]:
        """Enhanced action plan with domain awareness and logical sequencing"""
        steps = []
        domain_type = domain.get('type', 'unknown')
        
        # PHASE 1: CLEAN (high severity issues first)
        critical_points = [p for p in pain_points if p.get('severity') in ['critical', 'high']]
        for point in sorted(critical_points, key=lambda x: 0 if x.get('severity') == 'critical' else 1):
            fix = point.get('fix', '')
            steps.append(f"<strong>Clean:</strong> {fix}")
        
        # PHASE 2: VALIDATE (domain-specific)
        validation = self._get_domain_validation(domain_type)
        if validation:
            steps.append(f"<strong>Validate:</strong> {validation}")
        
        # PHASE 3: ANALYZE (domain-specific)
        analysis = self._get_domain_analysis(domain_type)
        if analysis:
            steps.append(f"<strong>Analyze:</strong> {analysis}")
        
        # PHASE 4: VISUALIZE
        viz = self._get_domain_visualization(domain_type)
        if viz:
            steps.append(f"<strong>Visualize:</strong> {viz}")
        
        # Fallback to generic if no steps
        if not steps:
            steps = [
                "<strong>Profile:</strong> Review column types and statistics",
                "<strong>Clean:</strong> Address any data quality issues",
                "<strong>Analyze:</strong> Calculate key metrics and trends",
                "<strong>Visualize:</strong> Create charts to communicate insights"
            ]
        
        return steps
    
    def _get_domain_validation(self, domain_type: str) -> str:
        """Get domain-specific validation checks"""
        validations = {
            'sales': "Verify all transactions have positive amounts and valid dates",
            'finance': "Ensure debits and credits balance correctly",
            'ecommerce': "Confirm order statuses are valid and payment amounts match totals",
            'marketing': "Validate campaign dates and ensure conversion rates are realistic",
            'healthcare': "Check patient IDs are unique and dates follow logical sequence",
            'hr': "Validate employee IDs are unique and hire dates precede termination dates",
            'inventory': "Ensure stock levels are non-negative and warehouse codes valid",
            'customer': "Check customer IDs are unique and contact info is properly formatted",
            'web_analytics': "Verify session IDs are unique and metrics are within realistic bounds",
            'logistics': "Validate tracking numbers are unique and delivery dates are after ship dates"
        }
        return validations.get(domain_type, "Check for logical errors and data inconsistencies")
    
    def _get_domain_analysis(self, domain_type: str) -> str:
        """Get domain-specific analysis recommendations"""
        analyses = {
            'sales': "Calculate total revenue, average order value, and identify top-selling products",
            'finance': "Calculate profit margin, ROI, and analyze expense trends",
            'ecommerce': "Calculate conversion rate, cart abandonment, and customer lifetime value",
            'marketing': "Calculate ROI per campaign and identify best-performing channels",
            'healthcare': "Calculate average length of stay and identify common diagnoses",
            'hr': "Calculate turnover rate and identify departments with highest attrition",
            'inventory': "Identify slow-moving items and calculate stock turnover ratio",
            'customer': "Calculate customer lifetime value and churn rate by segment",
            'web_analytics': "Identify high-bounce pages and analyze user journey funnels",
            'logistics': "Calculate average delivery time and identify late shipment patterns"
        }
        return analyses.get(domain_type, "Identify key metrics and trends relevant to your goals")
    
    def _get_domain_visualization(self, domain_type: str) -> str:
        """Get domain-specific visualization recommendations"""
        visualizations = {
            'sales': "Build revenue trend over time and product performance comparison",
            'finance': "Create P&L trend and expense breakdown charts",
            'ecommerce': "Chart sales funnel and customer acquisition cost trends",
            'marketing': "Visualize campaign ROI comparison and conversion funnel",
            'healthcare': "Plot patient flow by department and treatment outcomes",
            'hr': "Create headcount trend and turnover by department charts",
            'inventory': "Chart stock levels over time and turnover by product category",
            'customer': "Visualize customer journey map and satisfaction score trends",
            'web_analytics': "Build traffic trend and page performance heatmaps",
            'logistics': "Chart delivery time distribution and on-time percentage trends"
        }
        return visualizations.get(domain_type, "Create time series and distribution charts for key metrics")
    
    # ========================================================================
    # DAY 12: Fix Suggestions (ONLY 2 TYPES - CLEAN)
    # ========================================================================
    
    def generate_fix_suggestions(
        self,
        quality_report: Dict,
        profile: Dict
    ) -> List[Dict]:
        """
        Generate ONLY 2 fix suggestions for clean sidebar
        
        Returns: 1) Duplicates, 2) Missing values (worst column only)
        """
        suggestions = []
        
        # 1. DUPLICATES
        duplicate_count = quality_report.get('duplicates', 0)
        if duplicate_count > 0:
            severity = 'critical' if duplicate_count > 100 else 'high' if duplicate_count > 10 else 'medium'
            
            suggestions.append({
                'issue': f'{duplicate_count} duplicate rows detected',
                'severity': severity,
                'fix_method': 'remove_duplicates',
                'fix_args': {'keep': 'first'},
                'preview_impact': f'Will remove {duplicate_count} rows, keeping first occurrence',
                'button_text': 'Remove Duplicates',
                'icon': '🔄'
            })
        
        # 2. MISSING VALUES (worst column only)
        missing = quality_report.get('missing_by_column', {})
        column_types = {c.get('name'): c.get('type') for c in profile.get('columns', [])}
        
        if missing:
            # Find worst column
            worst_col = max(missing.items(), key=lambda x: x[1])
            col, count = worst_col
            
            if count > 0:
                row_count = profile.get('rows', profile.get('overall', {}).get('rows', 1))
                pct = (count / row_count) * 100
                
                if pct > 5:
                    col_type = column_types.get(col, 'object')
                    
                    if col_type in ['int64', 'float64', 'int32', 'float32', 'numeric']:
                        severity = 'critical' if pct > 20 else 'high' if pct > 10 else 'medium'
                        
                        suggestions.append({
                            'issue': f'{pct:.1f}% missing values in \'{col}\'',
                            'severity': severity,
                            'fix_method': 'fill_missing_numeric',
                            'fix_args': {'column': col, 'method': 'median'},
                            'preview_impact': f'Will fill {count} missing values with median',
                            'button_text': f'Fill {col} (median)',
                            'icon': '📊'
                        })
        
        return suggestions
    
    # ========================================================================
    # Full Narrative Generation
    # ========================================================================
    
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



if __name__ == "__main__":
    print("✅ Narrative Generator Ready (Days 7-9 + 12 - CLEAN SIDEBAR)")
