"""
Data Quality Report Generator - Enhanced with Visualizations
Exports profiling results as HTML and Markdown reports with visual elements
"""

from typing import Dict, Any
from datetime import datetime
import os


class QualityReportGenerator:
    """Generates data quality reports in multiple formats with visualizations"""
    
    def __init__(self, profile: Dict[str, Any], quality_report: Dict[str, Any]):
        self.profile = profile
        self.quality = quality_report
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def generate_markdown(self) -> str:
        """Generate Markdown report"""
        
        md = []
        md.append("# 📊 Data Quality Report\n")
        md.append(f"**Generated:** {self.timestamp}\n")
        md.append("---\n")
        
        # Overall Summary
        md.append("## 📈 Overall Summary\n")
        md.append(f"- **Rows:** {self.profile['overall']['rows']:,}")
        md.append(f"- **Columns:** {self.profile['overall']['columns']}")
        md.append(f"- **Memory:** {self.profile['overall']['memory_mb']:.2f} MB")
        md.append(f"- **Missing Data:** {self.profile['overall']['total_missing']:,} cells ({self.profile['overall']['total_missing_pct']:.1f}%)")
        md.append(f"- **Quality Score:** {self.quality['score']}/100 ({self.quality['status']})\n")
        
        # Column Type Summary
        md.append("## 📋 Column Types\n")
        for col_type, count in self.profile['type_summary'].items():
            md.append(f"- **{col_type.title()}:** {count} columns")
        md.append("")
        
        # Quality Assessment
        md.append("## ✅ Quality Assessment\n")
        
        if self.quality['score'] >= 90:
            md.append("🎉 **EXCELLENT** - Your data is in great shape!\n")
        elif self.quality['score'] >= 80:
            md.append("✅ **GOOD** - Your data quality is acceptable with minor issues.\n")
        elif self.quality['score'] >= 70:
            md.append("⚠️ **FAIR** - Your data has some quality issues that should be addressed.\n")
        else:
            md.append("🚨 **POOR** - Your data has serious quality issues requiring attention.\n")
        
        # Issues
        if self.quality['issues']:
            md.append("### 🚨 Critical Issues\n")
            for issue in self.quality['issues']:
                md.append(f"- {issue}")
            md.append("")
        
        # Warnings
        if self.quality['warnings']:
            md.append("### ⚠️ Warnings\n")
            for warning in self.quality['warnings']:
                md.append(f"- {warning}")
            md.append("")
        
        # Column Details
        md.append("## 📊 Column Details\n")
        md.append("| Column | Type | Missing | Unique | Issues |")
        md.append("|--------|------|---------|--------|--------|")
        
        for col in self.profile['columns']:
            issues_str = ', '.join(col['quality_issues']) if col['quality_issues'] else '-'
            md.append(f"| {col['name']} | {col['type']} | {col['missing_pct']:.1f}% | {col['unique']:,} | {issues_str} |")
        
        md.append("")
        
        # Correlations (if any)
        if self.profile.get('correlations'):
            md.append("## 🔗 High Correlations\n")
            for pair, corr in self.profile['correlations'].items():
                md.append(f"- **{pair}:** {corr:.3f}")
            md.append("")
        
        # Recommendations
        md.append("## 💡 Recommendations\n")
        
        recommendations = self._generate_recommendations()
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                md.append(f"{i}. {rec}")
        else:
            md.append("✅ No major recommendations - your data looks good!")
        
        md.append("")
        
        return '\n'.join(md)
    
    def generate_html(self) -> str:
        """Generate enhanced HTML report with visualizations"""
        
        # Score color and label
        if self.quality['score'] >= 90:
            score_color = '#22c55e'
            score_label = 'EXCELLENT'
            gauge_color = '#22c55e'
        elif self.quality['score'] >= 80:
            score_color = '#3b82f6'
            score_label = 'GOOD'
            gauge_color = '#3b82f6'
        elif self.quality['score'] >= 70:
            score_color = '#f59e0b'
            score_label = 'FAIR'
            gauge_color = '#f59e0b'
        else:
            score_color = '#ef4444'
            score_label = 'NEEDS WORK'
            gauge_color = '#ef4444'
        
        # Generate column type chart bars
        type_chart_html = self._generate_type_chart_html()
        
        # Generate missing data bars
        missing_data_html = self._generate_missing_data_html()
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Quality Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f8fafc;
            color: #1e293b;
            line-height: 1.6;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        }}
        .header h1 {{
            margin: 0 0 10px 0;
            font-size: 32px;
        }}
        .timestamp {{
            opacity: 0.9;
            font-size: 14px;
        }}
        .card {{
            background: white;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.12);
        }}
        .card h2 {{
            margin-bottom: 20px;
            color: #1e293b;
            font-size: 20px;
        }}
        
        /* Quality Score Gauge */
        .score-container {{
            text-align: center;
            padding: 20px;
        }}
        .gauge {{
            width: 200px;
            height: 200px;
            margin: 0 auto 20px;
            position: relative;
        }}
        .gauge-circle {{
            width: 100%;
            height: 100%;
            border-radius: 50%;
            background: conic-gradient(
                {gauge_color} 0deg,
                {gauge_color} {self.quality['score'] * 3.6}deg,
                #e2e8f0 {self.quality['score'] * 3.6}deg,
                #e2e8f0 360deg
            );
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        }}
        .gauge-inner {{
            width: 160px;
            height: 160px;
            background: white;
            border-radius: 50%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }}
        .score-value {{
            font-size: 48px;
            font-weight: bold;
            color: {score_color};
            line-height: 1;
        }}
        .score-max {{
            font-size: 20px;
            color: #64748b;
            margin-top: 4px;
        }}
        .score-label {{
            font-size: 18px;
            font-weight: 600;
            color: {score_color};
            margin-top: 12px;
        }}
        
        /* Metrics Grid */
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-top: 16px;
        }}
        .metric-box {{
            background: #f8fafc;
            padding: 16px;
            border-radius: 8px;
            border-left: 4px solid #3b82f6;
        }}
        .metric-label {{
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            color: #64748b;
            margin-bottom: 8px;
        }}
        .metric-value {{
            font-size: 24px;
            font-weight: bold;
            color: #1e293b;
        }}
        
        /* Column Type Chart */
        .type-chart {{
            margin-top: 20px;
        }}
        .type-bar {{
            display: flex;
            align-items: center;
            margin-bottom: 12px;
        }}
        .type-label {{
            width: 120px;
            font-weight: 600;
            font-size: 14px;
        }}
        .type-bar-container {{
            flex: 1;
            height: 32px;
            background: #f1f5f9;
            border-radius: 6px;
            overflow: hidden;
            position: relative;
            margin-right: 12px;
        }}
        .type-bar-fill {{
            height: 100%;
            background: linear-gradient(90deg, #3b82f6, #2563eb);
            border-radius: 6px;
            display: flex;
            align-items: center;
            padding-left: 12px;
            color: white;
            font-weight: 600;
            font-size: 13px;
            transition: width 0.6s ease;
        }}
        .type-count {{
            min-width: 40px;
            text-align: right;
            font-weight: 600;
            color: #64748b;
        }}
        
        /* Missing Data Visualization */
        .missing-viz {{
            margin-top: 20px;
        }}
        .missing-bar {{
            display: flex;
            align-items: center;
            margin-bottom: 8px;
            font-size: 13px;
        }}
        .col-name {{
            width: 200px;
            font-weight: 500;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}
        .missing-bar-container {{
            flex: 1;
            height: 24px;
            background: #f1f5f9;
            border-radius: 4px;
            overflow: hidden;
            margin: 0 8px;
        }}
        .missing-bar-fill {{
            height: 100%;
            border-radius: 4px;
            transition: width 0.6s ease;
        }}
        .missing-pct {{
            min-width: 50px;
            text-align: right;
            font-weight: 600;
        }}
        
        /* Issue Cards */
        .issue {{
            background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
            border-left: 4px solid #ef4444;
            padding: 16px;
            margin-bottom: 12px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(239, 68, 68, 0.1);
        }}
        .warning {{
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            border-left: 4px solid #f59e0b;
            padding: 16px;
            margin-bottom: 12px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(245, 158, 11, 0.1);
        }}
        .recommendation {{
            background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
            border-left: 4px solid #3b82f6;
            padding: 16px;
            margin-bottom: 12px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(59, 130, 246, 0.1);
        }}
        
        /* Table */
        table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            margin-top: 16px;
        }}
        th {{
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            padding: 12px;
            text-align: left;
            font-weight: 600;
            font-size: 13px;
            text-transform: uppercase;
            color: #475569;
            border-bottom: 2px solid #e2e8f0;
        }}
        th:first-child {{
            border-top-left-radius: 8px;
        }}
        th:last-child {{
            border-top-right-radius: 8px;
        }}
        td {{
            padding: 12px;
            border-bottom: 1px solid #e2e8f0;
            font-size: 14px;
        }}
        tr:hover {{
            background: #f8fafc;
        }}
        tr:last-child td {{
            border-bottom: none;
        }}
        
        /* Badges */
        .badge {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
        }}
        .badge-numeric {{ background: #dbeafe; color: #1e40af; }}
        .badge-categorical {{ background: #e9d5ff; color: #6b21a8; }}
        .badge-datetime {{ background: #fef3c7; color: #92400e; }}
        .badge-text {{ background: #d1fae5; color: #065f46; }}
        .badge-boolean {{ background: #fce7f3; color: #9f1239; }}
        .badge-id {{ background: #f3f4f6; color: #374151; }}
        
        /* Animation */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        .card {{
            animation: fadeIn 0.5s ease;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Data Quality Report</h1>
        <div class="timestamp">Generated: {self.timestamp}</div>
    </div>
    
    <!-- Quality Score Gauge -->
    <div class="card">
        <div class="score-container">
            <div class="gauge">
                <div class="gauge-circle">
                    <div class="gauge-inner">
                        <div class="score-value">{self.quality['score']}</div>
                        <div class="score-max">/100</div>
                    </div>
                </div>
            </div>
            <div class="score-label">{score_label}</div>
        </div>
    </div>
    
    <!-- Dataset Summary -->
    <div class="card">
        <h2>📈 Dataset Summary</h2>
        <div class="metrics-grid">
            <div class="metric-box">
                <div class="metric-label">Total Rows</div>
                <div class="metric-value">{self.profile['overall']['rows']:,}</div>
            </div>
            <div class="metric-box">
                <div class="metric-label">Total Columns</div>
                <div class="metric-value">{self.profile['overall']['columns']}</div>
            </div>
            <div class="metric-box">
                <div class="metric-label">Memory Usage</div>
                <div class="metric-value">{self.profile['overall']['memory_mb']:.1f} MB</div>
            </div>
            <div class="metric-box">
                <div class="metric-label">Missing Data</div>
                <div class="metric-value">{self.profile['overall']['total_missing_pct']:.1f}%</div>
            </div>
        </div>
    </div>
    
    <!-- Column Type Distribution -->
    <div class="card">
        <h2>📊 Column Type Distribution</h2>
        <div class="type-chart">
            {type_chart_html}
        </div>
    </div>
    
    <!-- Missing Data Visualization -->
    {missing_data_html}
"""
        
        # Issues
        if self.quality['issues']:
            html += '<div class="card"><h2>🚨 Critical Issues</h2>'
            for issue in self.quality['issues']:
                html += f'<div class="issue"><strong>⚠️</strong> {issue}</div>'
            html += '</div>'
        
        # Warnings
        if self.quality['warnings']:
            html += '<div class="card"><h2>⚠️ Warnings</h2>'
            for i, warning in enumerate(self.quality['warnings'][:10], 1):  # Show top 10
                html += f'<div class="warning"><strong>{i}.</strong> {warning}</div>'
            if len(self.quality['warnings']) > 10:
                html += f'<div class="warning"><em>... and {len(self.quality["warnings"]) - 10} more warnings</em></div>'
            html += '</div>'
        
        # Column details table
        html += '<div class="card"><h2>📋 Column Details</h2><table><thead><tr>'
        html += '<th>Column</th><th>Type</th><th>Missing</th><th>Unique</th><th>Issues</th>'
        html += '</tr></thead><tbody>'
        
        for col in self.profile['columns']:
            col_type_badge = f'badge-{col["type"]}'
            issues_str = ', '.join(col['quality_issues']) if col['quality_issues'] else '✓ No issues'
            html += f'''
            <tr>
                <td><strong>{col['name']}</strong></td>
                <td><span class="badge {col_type_badge}">{col['type']}</span></td>
                <td>{col['missing_pct']:.1f}%</td>
                <td>{col['unique']:,}</td>
                <td style="font-size: 12px; color: #64748b;">{issues_str}</td>
            </tr>
            '''
        
        html += '</tbody></table></div>'
        
        # Recommendations
        recommendations = self._generate_recommendations()
        if recommendations:
            html += '<div class="card"><h2>💡 Actionable Recommendations</h2>'
            for i, rec in enumerate(recommendations, 1):
                html += f'<div class="recommendation"><strong>{i}.</strong> {rec}</div>'
            html += '</div>'
        
        html += """
</body>
</html>
"""
        
        return html
    
    def _generate_type_chart_html(self) -> str:
        """Generate HTML for column type distribution chart"""
        max_count = max(self.profile['type_summary'].values()) if self.profile['type_summary'] else 1
        
        html_parts = []
        colors = {
            'numeric': '#3b82f6',
            'categorical': '#8b5cf6',
            'datetime': '#f59e0b',
            'text': '#10b981',
            'boolean': '#ec4899',
            'id': '#6b7280',
        }
        
        for col_type, count in sorted(self.profile['type_summary'].items(), key=lambda x: x[1], reverse=True):
            width_pct = (count / max_count) * 100
            color = colors.get(col_type, '#3b82f6')
            
            html_parts.append(f'''
            <div class="type-bar">
                <div class="type-label">{col_type.title()}</div>
                <div class="type-bar-container">
                    <div class="type-bar-fill" style="width: {width_pct}%; background: {color};">{count}</div>
                </div>
                <div class="type-count">{count}</div>
            </div>
            ''')
        
        return ''.join(html_parts)
    
    def _generate_missing_data_html(self) -> str:
        """Generate HTML for missing data visualization"""
        # Get columns with missing data
        cols_with_missing = [col for col in self.profile['columns'] if col['missing_pct'] > 0]
        
        if not cols_with_missing:
            return '<div class="card"><h2>✅ No Missing Data</h2><p>All columns are complete - excellent data quality!</p></div>'
        
        # Sort by missing percentage descending
        cols_with_missing.sort(key=lambda x: x['missing_pct'], reverse=True)
        
        html_parts = ['<div class="card"><h2>❓ Missing Data by Column</h2><div class="missing-viz">']
        
        for col in cols_with_missing[:15]:  # Show top 15
            missing_pct = col['missing_pct']
            
            # Color based on severity
            if missing_pct > 50:
                color = '#ef4444'  # Red
            elif missing_pct > 20:
                color = '#f59e0b'  # Orange
            else:
                color = '#3b82f6'  # Blue
            
            html_parts.append(f'''
            <div class="missing-bar">
                <div class="col-name" title="{col['name']}">{col['name']}</div>
                <div class="missing-bar-container">
                    <div class="missing-bar-fill" style="width: {missing_pct}%; background: {color};"></div>
                </div>
                <div class="missing-pct">{missing_pct:.1f}%</div>
            </div>
            ''')
        
        if len(cols_with_missing) > 15:
            html_parts.append(f'<p style="margin-top: 12px; color: #64748b; font-size: 13px;"><em>... and {len(cols_with_missing) - 15} more columns with missing data</em></p>')
        
        html_parts.append('</div></div>')
        
        return ''.join(html_parts)
    
    def _generate_recommendations(self) -> list:
        """Generate actionable recommendations based on quality report"""
        
        recommendations = []
        
        # High missing data
        high_missing_cols = [col['name'] for col in self.profile['columns'] 
                            if col['missing_pct'] > 50]
        if high_missing_cols:
            recommendations.append(
                f"🔴 **High missing data:** Consider removing or imputing columns: {', '.join(high_missing_cols[:3])}"
            )
        
        # Constant columns
        constant_cols = [col['name'] for col in self.profile['columns'] 
                        if col['unique'] == 1]
        if constant_cols:
            recommendations.append(
                f"🔴 **Constant columns:** Remove these columns as they provide no information: {', '.join(constant_cols)}"
            )
        
        # High cardinality categoricals
        high_card_cols = [col['name'] for col in self.profile['columns'] 
                         if 'HIGH_CARDINALITY' in col['quality_issues']]
        if high_card_cols:
            recommendations.append(
                f"🟡 **High cardinality:** Consider grouping rare categories in: {', '.join(high_card_cols[:3])}"
            )
        
        # Many outliers
        outlier_cols = [col['name'] for col in self.profile['columns'] 
                       if 'MANY_OUTLIERS' in col['quality_issues']]
        if outlier_cols:
            recommendations.append(
                f"🟡 **Outliers detected:** Review and handle outliers in: {', '.join(outlier_cols[:3])}"
            )
        
        # Good quality
        if self.quality['score'] >= 90:
            recommendations.append("✅ **Great data quality!** Your dataset is ready for analysis.")
        
        return recommendations
    
    def save_markdown(self, filepath: str):
        """Save report as Markdown file"""
        md_content = self.generate_markdown()
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"✅ Markdown report saved: {filepath}")
    
    def save_html(self, filepath: str):
        """Save report as HTML file"""
        html_content = self.generate_html()
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✅ HTML report saved: {filepath}")
    
    def save_both(self, base_filename: str, output_dir: str = 'output'):
        """Save both Markdown and HTML reports"""
        os.makedirs(output_dir, exist_ok=True)
        
        md_path = os.path.join(output_dir, f"{base_filename}.md")
        html_path = os.path.join(output_dir, f"{base_filename}.html")
        
        self.save_markdown(md_path)
        self.save_html(html_path)
        
        return md_path, html_path
