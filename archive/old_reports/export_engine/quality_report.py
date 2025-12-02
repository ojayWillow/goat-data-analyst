"""
PRODUCTION-GRADE Data Quality Report Generator v2.0

This module generates interactive, professional data quality reports
with full download functionality, filtering, sorting, and export capabilities.

Features:
- Interactive HTML reports with gauges and visualizations
- Multiple export formats (CSV, JSON, HTML)
- Real-time search and filtering
- Sortable tables
- Copy to clipboard
- Print-friendly design
- Mobile responsive
- Comprehensive error handling

Author: GOAT Data Analyst Project
Version: 2.0
Last Updated: 2025-11-27
"""

from typing import Dict, Any, List, Tuple
from datetime import datetime
import os
import json
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ReportConfig:
    """Configuration constants for report generation"""
    
    # Score thresholds
    EXCELLENT_THRESHOLD = 90
    GOOD_THRESHOLD = 80
    FAIR_THRESHOLD = 70
    
    # Colors (green gauge for excellent)
    COLORS = {
        'excellent': '#22c55e',  # Green
        'good': '#3b82f6',       # Blue
        'fair': '#f59e0b',       # Orange
        'poor': '#ef4444',       # Red
        'numeric': '#3b82f6',
        'categorical': '#8b5cf6',
        'datetime': '#f59e0b',
        'text': '#10b981',
        'boolean': '#ec4899',
        'id': '#6b7280',
    }
    
    # Labels
    SCORE_LABELS = {
        'excellent': 'EXCELLENT',
        'good': 'GOOD',
        'fair': 'FAIR',
        'poor': 'NEEDS WORK'
    }
    
    # Display limits
    MAX_WARNINGS_DISPLAY = 10
    MAX_MISSING_COLS_DISPLAY = 15
    MAX_RECOMMENDATIONS = 10
    
    # Thresholds
    HIGH_MISSING_THRESHOLD = 50
    MODERATE_MISSING_THRESHOLD = 20


class QualityReportGenerator:
    """
    Generates professional data quality reports in multiple formats.
    
    This class creates interactive HTML reports and markdown summaries
    from data profile and quality assessment information.
    
    Attributes:
        profile (Dict[str, Any]): Data profiling information
        quality (Dict[str, Any]): Quality assessment results
        timestamp (str): Report generation timestamp
        config (ReportConfig): Configuration constants
    """
    
    def __init__(self, profile: Dict[str, Any], quality_report: Dict[str, Any]):
        """
        Initialize the report generator.
        
        Args:
            profile: Dictionary containing data profiling information
            quality_report: Dictionary containing quality assessment results
        """
        self.profile = profile
        self.quality = quality_report
        self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.config = ReportConfig()
        
        logger.info(f"QualityReportGenerator initialized with score: {self.quality['score']}")
    
    def _get_score_category(self) -> str:
        """
        Determine the score category based on quality score.
        
        Returns:
            str: Category name ('excellent', 'good', 'fair', or 'poor')
        """
        score = self.quality['score']
        if score >= self.config.EXCELLENT_THRESHOLD:
            return 'excellent'
        elif score >= self.config.GOOD_THRESHOLD:
            return 'good'
        elif score >= self.config.FAIR_THRESHOLD:
            return 'fair'
        else:
            return 'poor'
    
    def _get_score_color(self) -> str:
        """Get the color for the current score category."""
        category = self._get_score_category()
        return self.config.COLORS[category]
    
    def _get_score_label(self) -> str:
        """Get the label for the current score category."""
        category = self._get_score_category()
        return self.config.SCORE_LABELS[category]
    
    def _sanitize_html(self, text: str) -> str:
        """
        Sanitize text for safe HTML output.
        
        Args:
            text: Input text to sanitize
            
        Returns:
            str: Sanitized text safe for HTML
        """
        if not isinstance(text, str):
            text = str(text)
        
        return (text
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&#x27;'))
    
    def _generate_recommendations(self) -> List[str]:
        """
        Generate actionable recommendations based on data quality.
        
        Returns:
            List[str]: List of recommendation strings
        """
        recommendations = []
        
        # High missing data
        high_missing_cols = [
            col['name'] for col in self.profile['columns']
            if col['missing_pct'] > self.config.HIGH_MISSING_THRESHOLD
        ]
        if high_missing_cols:
            cols_str = ', '.join(high_missing_cols[:3])
            if len(high_missing_cols) > 3:
                cols_str += f" (+{len(high_missing_cols) - 3} more)"
            recommendations.append(
                f" **High missing data:** {cols_str}. "
                f"Consider imputation or investigate data collection issues."
            )
        
        # Constant columns
        constant_cols = [
            col['name'] for col in self.profile['columns']
            if col['unique'] == 1
        ]
        if constant_cols:
            recommendations.append(
                f" **Constant columns detected:** {', '.join(constant_cols)}. "
                f"These provide no information and should be removed."
            )
        
        # High cardinality
        high_card_cols = [
            col['name'] for col in self.profile['columns']
            if 'HIGH_CARDINALITY' in col['quality_issues']
        ]
        if high_card_cols:
            cols_str = ', '.join(high_card_cols[:3])
            if len(high_card_cols) > 3:
                cols_str += f" (+{len(high_card_cols) - 3} more)"
            recommendations.append(
                f" **High cardinality columns:** {cols_str}. "
                f"Consider grouping or binning for analysis."
            )
        
        # Outliers
        outlier_cols = [
            col['name'] for col in self.profile['columns']
            if 'MANY_OUTLIERS' in col['quality_issues']
        ]
        if outlier_cols:
            cols_str = ', '.join(outlier_cols[:3])
            if len(outlier_cols) > 3:
                cols_str += f" (+{len(outlier_cols) - 3} more)"
            recommendations.append(
                f" **Outliers detected:** {cols_str}. "
                f"Review for data entry errors or valid edge cases."
            )
        
        # Moderate missing data
        moderate_missing_cols = [
            col['name'] for col in self.profile['columns']
            if self.config.MODERATE_MISSING_THRESHOLD < col['missing_pct'] <= self.config.HIGH_MISSING_THRESHOLD
        ]
        if moderate_missing_cols and len(recommendations) < 5:
            cols_str = ', '.join(moderate_missing_cols[:3])
            if len(moderate_missing_cols) > 3:
                cols_str += f" (+{len(moderate_missing_cols) - 3} more)"
            recommendations.append(
                f" **Moderate missing data:** {cols_str}. "
                f"Monitor these columns during analysis."
            )
        
        # Positive feedback for high quality
        if self.quality['score'] >= self.config.EXCELLENT_THRESHOLD:
            recommendations.append(
                " **Excellent data quality!** Your dataset is clean and ready for analysis. "
                "No critical issues detected."
            )
        elif self.quality['score'] >= self.config.GOOD_THRESHOLD and not recommendations:
            recommendations.append(
                " **Good data quality!** Minor issues detected but dataset is suitable for analysis."
            )
        
        return recommendations[:self.config.MAX_RECOMMENDATIONS]
    
    def generate_markdown(self) -> str:
        """
        Generate a comprehensive Markdown report.
        
        Returns:
            str: Markdown-formatted report
        """
        logger.info("Generating Markdown report")
        
        md = []
        md.append("#  Data Quality Report\n")
        md.append(f"**Generated:** {self.timestamp}\n")
        md.append("---\n")
        
        # Overall Summary
        md.append("##  Overall Summary\n")
        md.append(f"- **Rows:** {self.profile['overall']['rows']:,}")
        md.append(f"- **Columns:** {self.profile['overall']['columns']}")
        md.append(f"- **Memory:** {self.profile['overall']['memory_mb']:.2f} MB")
        md.append(f"- **Missing Data:** {self.profile['overall']['total_missing']:,} cells "
                  f"({self.profile['overall']['total_missing_pct']:.1f}%)")
        md.append(f"- **Quality Score:** {self.quality['score']}/100 "
                  f"({self._get_score_label()})\n")
        
        # Column Type Summary
        md.append("##  Column Types\n")
        for col_type, count in sorted(self.profile['type_summary'].items()):
            md.append(f"- **{col_type.title()}:** {count} columns")
        md.append("")
        
        # Quality Assessment
        md.append("##  Quality Assessment\n")
        score = self.quality['score']
        
        if score >= self.config.EXCELLENT_THRESHOLD:
            md.append(" **EXCELLENT** - Your data is in great shape!\n")
        elif score >= self.config.GOOD_THRESHOLD:
            md.append(" **GOOD** - Your data quality is acceptable with minor issues.\n")
        elif score >= self.config.FAIR_THRESHOLD:
            md.append(" **FAIR** - Your data has some quality issues that should be addressed.\n")
        else:
            md.append(" **POOR** - Your data has serious quality issues requiring immediate attention.\n")
        
        # Issues
        if self.quality['issues']:
            md.append("###  Critical Issues\n")
            for i, issue in enumerate(self.quality['issues'], 1):
                md.append(f"{i}. {issue}")
            md.append("")
        
        # Warnings
        if self.quality['warnings']:
            md.append("###  Warnings\n")
            for i, warning in enumerate(self.quality['warnings'][:self.config.MAX_WARNINGS_DISPLAY], 1):
                md.append(f"{i}. {warning}")
            if len(self.quality['warnings']) > self.config.MAX_WARNINGS_DISPLAY:
                remaining = len(self.quality['warnings']) - self.config.MAX_WARNINGS_DISPLAY
                md.append(f"\n*... and {remaining} more warnings*")
            md.append("")
        
        # Column Details
        md.append("##  Column Details\n")
        md.append("| Column | Type | Missing | Unique | Issues |")
        md.append("|--------|------|---------|--------|--------|")
        
        for col in self.profile['columns']:
            issues_str = ', '.join(col['quality_issues']) if col['quality_issues'] else '-'
            md.append(
                f"| {col['name']} | {col['type']} | "
                f"{col['missing_pct']:.1f}% | {col['unique']:,} | {issues_str} |"
            )
        
        md.append("")
        
        # Recommendations
        md.append("##  Recommendations\n")
        recommendations = self._generate_recommendations()
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                md.append(f"{i}. {rec}")
        else:
            md.append(" No major recommendations - your data looks good!")
        
        md.append("")
        md.append("---")
        md.append(f"\n*Report generated by GOAT Data Analyst v2.0 on {self.timestamp}*\n")
        
        logger.info("Markdown report generated successfully")
        return '\n'.join(md)
    
    def _generate_type_chart_html(self) -> str:
        """Generate HTML for column type distribution visualization."""
        if not self.profile['type_summary']:
            return '<p style="color: #64748b;">No type information available</p>'
        
        max_count = max(self.profile['type_summary'].values())
        html_parts = []
        
        for col_type, count in sorted(
            self.profile['type_summary'].items(),
            key=lambda x: x[1],
            reverse=True
        ):
            width_pct = (count / max_count) * 100
            color = self.config.COLORS.get(col_type, '#3b82f6')
            
            html_parts.append(
                f'<div class="type-bar" data-type="{col_type}">'
                f'<div class="type-label">{col_type.title()}</div>'
                f'<div class="type-bar-container">'
                f'<div class="type-bar-fill" style="width: {width_pct}%; background: {color};">'
                f'{count}'
                f'</div>'
                f'</div>'
                f'<div class="type-count">{count}</div>'
                f'</div>'
            )
        
        return ''.join(html_parts)
    
    def _generate_missing_data_html(self) -> str:
        """Generate HTML for missing data visualization."""
        cols_with_missing = [
            col for col in self.profile['columns']
            if col['missing_pct'] > 0
        ]
        
        if not cols_with_missing:
            return '<div class="card"><h2> No Missing Data</h2><p style="color: #64748b;">All columns are complete!</p></div>'
        
        cols_with_missing.sort(key=lambda x: x['missing_pct'], reverse=True)
        
        html_parts = [
            '<div class="card">',
            '<h2> Missing Data by Column</h2>',
            '<div class="missing-viz">'
        ]
        
        display_limit = min(len(cols_with_missing), self.config.MAX_MISSING_COLS_DISPLAY)
        
        for col in cols_with_missing[:display_limit]:
            missing_pct = col['missing_pct']
            
            # Color based on severity
            if missing_pct > self.config.HIGH_MISSING_THRESHOLD:
                color = self.config.COLORS['poor']
            elif missing_pct > self.config.MODERATE_MISSING_THRESHOLD:
                color = self.config.COLORS['fair']
            else:
                color = self.config.COLORS['good']
            
            col_name_safe = self._sanitize_html(col['name'])
            
            html_parts.append(
                f'<div class="missing-bar">'
                f'<div class="col-name" title="{col_name_safe}">{col_name_safe}</div>'
                f'<div class="missing-bar-container">'
                f'<div class="missing-bar-fill" style="width: {missing_pct}%; background: {color};"></div>'
                f'</div>'
                f'<div class="missing-pct">{missing_pct:.1f}%</div>'
                f'</div>'
            )
        
        if len(cols_with_missing) > display_limit:
            remaining = len(cols_with_missing) - display_limit
            html_parts.append(
                f'<p style="margin-top: 12px; color: #64748b; font-size: 13px;">'
                f'<em>... and {remaining} more column{"s" if remaining > 1 else ""} with missing data</em>'
                f'</p>'
            )
        
        html_parts.extend(['</div>', '</div>'])
        
        return ''.join(html_parts)
    
    def _generate_table_rows_html(self) -> str:
        """Generate HTML table rows for column details."""
        rows = []
        
        for col in self.profile['columns']:
            col_type = col['type']
            col_type_badge = f'badge-{col_type}'
            
            # Sanitize column name
            col_name_safe = self._sanitize_html(col['name'])
            
            # Format issues
            if col['quality_issues']:
                issues_str = self._sanitize_html(', '.join(col['quality_issues']))
            else:
                issues_str = ''
            
            rows.append(
                f'<tr data-type="{col_type}">'
                f'<td><strong>{col_name_safe}</strong></td>'
                f'<td><span class="badge {col_type_badge}">{col_type}</span></td>'
                f'<td>{col["missing_pct"]:.1f}%</td>'
                f'<td>{col["unique"]:,}</td>'
                f'<td style="font-size: 12px; color: #64748b;">{issues_str}</td>'
                f'</tr>'
            )
        
        return '\n'.join(rows)
    
    def _get_css_styles(self) -> str:
        """Get complete CSS styles for the HTML report."""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f8fafc;
            color: #1e293b;
            line-height: 1.6;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        }
        
        .header h1 {
            margin: 0 0 10px 0;
            font-size: 32px;
            font-weight: 700;
        }
        
        .timestamp {
            opacity: 0.9;
            font-size: 14px;
        }
        
        .card {
            background: white;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.12);
        }
        
        .card h2 {
            margin-bottom: 20px;
            color: #1e293b;
            font-size: 20px;
            font-weight: 600;
        }
        
        .score-container {
            text-align: center;
            padding: 20px;
        }
        
        .gauge {
            width: 200px;
            height: 200px;
            margin: 0 auto 20px;
            position: relative;
        }
        
        .gauge-circle {
            width: 100%;
            height: 100%;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        }
        
        .gauge-inner {
            width: 160px;
            height: 160px;
            background: white;
            border-radius: 50%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            box-shadow: inset 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .score-value {
            font-size: 48px;
            font-weight: 700;
            line-height: 1;
        }
        
        .score-max {
            font-size: 20px;
            color: #64748b;
            margin-top: 4px;
        }
        
        .score-label {
            font-size: 18px;
            font-weight: 600;
            margin-top: 12px;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-top: 16px;
        }
        
        .metric-box {
            background: #f8fafc;
            padding: 16px;
            border-radius: 8px;
            border-left: 4px solid #3b82f6;
            transition: all 0.2s;
        }
        
        .metric-box:hover {
            background: #f1f5f9;
            transform: translateX(4px);
        }
        
        .metric-label {
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            color: #64748b;
            margin-bottom: 8px;
        }
        
        .metric-value {
            font-size: 24px;
            font-weight: 700;
            color: #1e293b;
        }
        
        .type-bar {
            display: flex;
            align-items: center;
            margin-bottom: 12px;
            cursor: pointer;
            padding: 8px;
            border-radius: 6px;
            transition: background 0.2s;
        }
        
        .type-bar:hover {
            background: #f8fafc;
        }
        
        .type-bar.active {
            background: #e0e7ff;
            border-left: 3px solid #3b82f6;
        }
        
        .type-label {
            width: 120px;
            font-weight: 600;
            font-size: 14px;
        }
        
        .type-bar-container {
            flex: 1;
            height: 32px;
            background: #f1f5f9;
            border-radius: 6px;
            overflow: hidden;
            position: relative;
            margin-right: 12px;
        }
        
        .type-bar-fill {
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
        }
        
        .type-count {
            min-width: 40px;
            text-align: right;
            font-weight: 600;
            color: #64748b;
        }
        
        .missing-bar {
            display: flex;
            align-items: center;
            margin-bottom: 8px;
            font-size: 13px;
        }
        
        .col-name {
            width: 200px;
            font-weight: 500;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        
        .missing-bar-container {
            flex: 1;
            height: 24px;
            background: #f1f5f9;
            border-radius: 4px;
            overflow: hidden;
            margin: 0 8px;
        }
        
        .missing-bar-fill {
            height: 100%;
            border-radius: 4px;
            transition: width 0.6s ease;
        }
        
        .missing-pct {
            min-width: 50px;
            text-align: right;
            font-weight: 600;
        }
        
        .issue {
            background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
            border-left: 4px solid #ef4444;
            padding: 16px;
            margin-bottom: 12px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(239, 68, 68, 0.1);
        }
        
        .warning {
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
            border-left: 4px solid #f59e0b;
            padding: 16px;
            margin-bottom: 12px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(245, 158, 11, 0.1);
        }
        
        .recommendation {
            background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
            border-left: 4px solid #3b82f6;
            padding: 16px;
            margin-bottom: 12px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(59, 130, 246, 0.1);
        }
        
        .controls {
            display: flex;
            gap: 12px;
            margin-bottom: 16px;
            flex-wrap: wrap;
        }
        
        .search-box {
            flex: 1;
            min-width: 200px;
            padding: 12px 16px;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            font-size: 14px;
            transition: border-color 0.2s;
        }
        
        .search-box:focus {
            outline: none;
            border-color: #3b82f6;
        }
        
        .btn {
            padding: 12px 24px;
            background: linear-gradient(135deg, #3b82f6, #2563eb);
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            font-size: 14px;
            box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
            transition: all 0.2s;
            white-space: nowrap;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
        }
        
        .btn:active {
            transform: translateY(0);
        }
        
        .btn-secondary {
            background: linear-gradient(135deg, #64748b, #475569);
        }
        
        .btn-success {
            background: linear-gradient(135deg, #22c55e, #16a34a);
        }
        
        .table-container {
            overflow-x: auto;
        }
        
        table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            margin-top: 16px;
        }
        
        th {
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            padding: 12px;
            text-align: left;
            font-weight: 600;
            font-size: 13px;
            text-transform: uppercase;
            color: #475569;
            border-bottom: 2px solid #e2e8f0;
            cursor: pointer;
            user-select: none;
            transition: background 0.2s;
        }
        
        th:hover {
            background: #e2e8f0;
        }
        
        th:first-child {
            border-top-left-radius: 8px;
        }
        
        th:last-child {
            border-top-right-radius: 8px;
        }
        
        th::after {
            content: ' ';
            opacity: 0.3;
        }
        
        td {
            padding: 12px;
            border-bottom: 1px solid #e2e8f0;
            font-size: 14px;
        }
        
        tr:hover {
            background: #f8fafc;
        }
        
        tr:last-child td {
            border-bottom: none;
        }
        
        tr.hidden {
            display: none;
        }
        
        .badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
        }
        
        .badge-numeric { background: #dbeafe; color: #1e40af; }
        .badge-categorical { background: #e9d5ff; color: #6b21a8; }
        .badge-datetime { background: #fef3c7; color: #92400e; }
        .badge-text { background: #d1fae5; color: #065f46; }
        .badge-boolean { background: #fce7f3; color: #9f1239; }
        .badge-id { background: #f3f4f6; color: #374151; }
        
        .filter-info {
            padding: 12px;
            background: #eff6ff;
            border-left: 4px solid #3b82f6;
            border-radius: 6px;
            margin-bottom: 16px;
            font-size: 14px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .filter-info button {
            background: #3b82f6;
            color: white;
            border: none;
            padding: 6px 16px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            font-weight: 600;
        }
        
        .filter-info button:hover {
            background: #2563eb;
        }
        
        .toast {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 16px 24px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            display: none;
            align-items: center;
            gap: 12px;
            z-index: 1000;
            animation: slideIn 0.3s ease;
        }
        
        .toast.show {
            display: flex;
        }
        
        .toast-success {
            border-left: 4px solid #22c55e;
        }
        
        .toast-error {
            border-left: 4px solid #ef4444;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        .card {
            animation: fadeIn 0.5s ease;
        }
        
        @media print {
            body {
                background: white;
                padding: 0;
            }
            
            .card {
                box-shadow: none;
                page-break-inside: avoid;
            }
            
            .btn {
                display: none;
            }
            
            .search-box {
                display: none;
            }
            
            .header {
                background: #667eea;
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }
        }
        
        @media (max-width: 768px) {
            body {
                padding: 10px;
            }
            
            .header {
                padding: 20px;
            }
            
            .header h1 {
                font-size: 24px;
            }
            
            .card {
                padding: 16px;
            }
            
            .metrics-grid {
                grid-template-columns: 1fr;
            }
            
            .gauge {
                width: 150px;
                height: 150px;
            }
            
            .gauge-inner {
                width: 120px;
                height: 120px;
            }
            
            .score-value {
                font-size: 36px;
            }
            
            .controls {
                flex-direction: column;
            }
            
            .btn {
                width: 100%;
            }
            
            .type-label {
                width: 80px;
                font-size: 12px;
            }
            
            .col-name {
                width: 100px;
            }
            
            table {
                font-size: 12px;
            }
            
            th, td {
                padding: 8px 6px;
            }
        }
        """
    
    def _get_javascript_code(self) -> str:
        """Get complete JavaScript code for interactive features."""
        return """
        let currentFilter = null;
        let sortDirection = {};
        
        function showToast(message, type = 'success') {
            const toast = document.getElementById('toast');
            const toastMessage = document.getElementById('toastMessage');
            
            toastMessage.textContent = message;
            toast.className = `toast toast-${type} show`;
            
            setTimeout(() => {
                toast.classList.remove('show');
            }, 3000);
        }
        
        document.querySelectorAll('.type-bar').forEach(bar => {
            bar.addEventListener('click', function() {
                const type = this.dataset.type;
                if (currentFilter === type) {
                    clearFilter();
                } else {
                    filterByType(type);
                }
            });
        });
        
        function filterByType(type) {
            try {
                currentFilter = type;
                
                document.querySelectorAll('.type-bar').forEach(b => {
                    b.classList.toggle('active', b.dataset.type === type);
                });
                
                const rows = document.querySelectorAll('#dataTable tr');
                let visibleCount = 0;
                
                rows.forEach(row => {
                    if (row.dataset.type === type) {
                        row.classList.remove('hidden');
                        visibleCount++;
                    } else {
                        row.classList.add('hidden');
                    }
                });
                
                document.getElementById('filterInfo').style.display = 'flex';
                document.getElementById('filterType').textContent = `${type} (${visibleCount} columns)`;
                
                showToast(`Filtered to ${visibleCount} ${type} columns`, 'success');
            } catch (error) {
                console.error('Filter error:', error);
                showToast('Error applying filter', 'error');
            }
        }
        
        function clearFilter() {
            try {
                currentFilter = null;
                
                document.querySelectorAll('.type-bar').forEach(b => {
                    b.classList.remove('active');
                });
                
                document.querySelectorAll('#dataTable tr').forEach(row => {
                    row.classList.remove('hidden');
                });
                
                document.getElementById('filterInfo').style.display = 'none';
                document.getElementById('searchBox').value = '';
                
                showToast('Filter cleared', 'success');
            } catch (error) {
                console.error('Clear filter error:', error);
            }
        }
        
        document.getElementById('searchBox').addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            
            document.querySelectorAll('#dataTable tr').forEach(row => {
                const text = row.textContent.toLowerCase();
                const matchesSearch = !searchTerm || text.includes(searchTerm);
                const matchesFilter = !currentFilter || row.dataset.type === currentFilter;
                
                if (matchesSearch && matchesFilter) {
                    row.classList.remove('hidden');
                } else {
                    row.classList.add('hidden');
                }
            });
        });
        
        function sortTable(columnIndex) {
            try {
                const table = document.getElementById('dataTable');
                const rows = Array.from(table.rows);
                
                if (!sortDirection[columnIndex]) {
                    sortDirection[columnIndex] = 'asc';
                } else {
                    sortDirection[columnIndex] = sortDirection[columnIndex] === 'asc' ? 'desc' : 'asc';
                }
                
                const direction = sortDirection[columnIndex];
                
                rows.sort((a, b) => {
                    let aValue = a.cells[columnIndex].textContent.trim();
                    let bValue = b.cells[columnIndex].textContent.trim();
                    
                    if (columnIndex === 2 || columnIndex === 3) {
                        aValue = parseFloat(aValue.replace(/[^0-9.-]/g, '')) || 0;
                        bValue = parseFloat(bValue.replace(/[^0-9.-]/g, '')) || 0;
                    }
                    
                    if (direction === 'asc') {
                        return aValue > bValue ? 1 : -1;
                    } else {
                        return aValue < bValue ? 1 : -1;
                    }
                });
                
                rows.forEach(row => table.appendChild(row));
                
                showToast(`Sorted by column ${columnIndex + 1} (${direction})`, 'success');
            } catch (error) {
                console.error('Sort error:', error);
                showToast('Error sorting table', 'error');
            }
        }
        
        function exportTableToCSV() {
            try {
                const table = document.getElementById('dataTable');
                const headers = ['Column', 'Type', 'Missing %', 'Unique', 'Issues'];
                
                const rows = Array.from(table.querySelectorAll('tr'))
                    .filter(row => !row.classList.contains('hidden'));
                
                if (rows.length === 0) {
                    showToast('No data to export', 'error');
                    return;
                }
                
                let csv = headers.join(',') + '\\n';
                
                rows.forEach(row => {
                    const cells = row.querySelectorAll('td');
                    const rowData = Array.from(cells).map(cell => {
                        let text = cell.textContent.trim().replace(/\\s+/g, ' ');
                        
                        if (text.includes(',') || text.includes('"') || text.includes('\\n')) {
                            text = '"' + text.replace(/"/g, '""') + '"';
                        }
                        
                        return text;
                    });
                    
                    csv += rowData.join(',') + '\\n';
                });
                
                const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
                const url = URL.createObjectURL(blob);
                const link = document.createElement('a');
                const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
                
                link.href = url;
                link.download = `quality_report_${timestamp}.csv`;
                link.style.display = 'none';
                
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                
                URL.revokeObjectURL(url);
                
                showToast(`Exported ${rows.length} rows to CSV`, 'success');
            } catch (error) {
                console.error('Export error:', error);
                showToast(`Export failed: ${error.message}`, 'error');
            }
        }
        
        function exportToJSON() {
            try {
                const table = document.getElementById('dataTable');
                const rows = Array.from(table.querySelectorAll('tr'))
                    .filter(row => !row.classList.contains('hidden'));
                
                if (rows.length === 0) {
                    showToast('No data to export', 'error');
                    return;
                }
                
                const data = rows.map(row => {
                    const cells = row.querySelectorAll('td');
                    return {
                        column: cells[0].textContent.trim(),
                        type: cells[1].textContent.trim(),
                        missing_pct: cells[2].textContent.trim(),
                        unique: cells[3].textContent.trim(),
                        issues: cells[4].textContent.trim()
                    };
                });
                
                const json = JSON.stringify(data, null, 2);
                const blob = new Blob([json], { type: 'application/json' });
                const url = URL.createObjectURL(blob);
                const link = document.createElement('a');
                const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
                
                link.href = url;
                link.download = `quality_report_${timestamp}.json`;
                link.style.display = 'none';
                
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                
                URL.revokeObjectURL(url);
                
                showToast(`Exported ${rows.length} rows to JSON`, 'success');
            } catch (error) {
                console.error('JSON export error:', error);
                showToast(`Export failed: ${error.message}`, 'error');
            }
        }
        
        function copyToClipboard() {
            try {
                const table = document.getElementById('dataTable');
                const rows = Array.from(table.querySelectorAll('tr'))
                    .filter(row => !row.classList.contains('hidden'));
                
                if (rows.length === 0) {
                    showToast('No data to copy', 'error');
                    return;
                }
                
                const headers = 'Column\\tType\\tMissing %\\tUnique\\tIssues';
                const data = rows.map(row => {
                    const cells = Array.from(row.querySelectorAll('td'));
                    return cells.map(cell => cell.textContent.trim()).join('\\t');
                }).join('\\n');
                
                const textData = headers + '\\n' + data;
                
                navigator.clipboard.writeText(textData).then(() => {
                    showToast(`Copied ${rows.length} rows to clipboard`, 'success');
                }).catch(err => {
                    showToast('Failed to copy to clipboard', 'error');
                    console.error('Clipboard error:', err);
                });
            } catch (error) {
                console.error('Copy error:', error);
                showToast(`Copy failed: ${error.message}`, 'error');
            }
        }
        
        function downloadHTMLReport() {
            try {
                const htmlContent = document.documentElement.outerHTML;
                const blob = new Blob([htmlContent], { type: 'text/html' });
                const url = URL.createObjectURL(blob);
                const link = document.createElement('a');
                const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
                
                link.href = url;
                link.download = `quality_report_full_${timestamp}.html`;
                link.style.display = 'none';
                
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                
                URL.revokeObjectURL(url);
                
                showToast('Full HTML report downloaded', 'success');
            } catch (error) {
                console.error('HTML download error:', error);
                showToast(`Download failed: ${error.message}`, 'error');
            }
        }
        
        document.addEventListener('DOMContentLoaded', function() {
            console.log('Quality Report v2.0 loaded successfully');
        });
        """
    
    def generate_html(self) -> str:
        """Generate a fully interactive HTML report with all features."""
        logger.info("Generating HTML report")
        
        try:
            score_color = self._get_score_color()
            score_label = self._get_score_label()
            score = self.quality['score']
            
            type_chart_html = self._generate_type_chart_html()
            missing_data_html = self._generate_missing_data_html()
            table_rows_html = self._generate_table_rows_html()
            
            html_parts = []
            
            html_parts.append(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Interactive Data Quality Report - GOAT Data Analyst v2.0">
    <title>Data Quality Report - Score: {score}/100</title>
    <style>
        {self._get_css_styles()}
    </style>
</head>
<body>
    <div id="toast" class="toast">
        <span id="toastMessage"></span>
    </div>
    
    <div class="header">
        <h1> Data Quality Report</h1>
        <div class="timestamp">Generated: {self.timestamp}</div>
    </div>
    
    <div class="card">
        <div class="score-container">
            <div class="gauge">
                <div class="gauge-circle" style="background: conic-gradient(
                    {score_color} 0deg,
                    {score_color} {score * 3.6}deg,
                    #e2e8f0 {score * 3.6}deg,
                    #e2e8f0 360deg
                );">
                    <div class="gauge-inner">
                        <div class="score-value" style="color: {score_color};">{score}</div>
                        <div class="score-max">/100</div>
                    </div>
                </div>
            </div>
            <div class="score-label" style="color: {score_color};">{score_label}</div>
        </div>
    </div>
    
    <div class="card">
        <h2> Dataset Summary</h2>
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
    
    <div class="card">
        <h2> Column Type Distribution (Click to Filter)</h2>
        <div class="type-chart">
            {type_chart_html}
        </div>
    </div>
    
    {missing_data_html}
""")
            
            if self.quality.get('issues'):
                html_parts.append('<div class="card"><h2> Critical Issues</h2>')
                for issue in self.quality['issues']:
                    issue_safe = self._sanitize_html(issue)
                    html_parts.append(f'<div class="issue"><strong></strong> {issue_safe}</div>')
                html_parts.append('</div>')
            
            if self.quality.get('warnings'):
                html_parts.append('<div class="card"><h2> Warnings</h2>')
                display_warnings = self.quality['warnings'][:self.config.MAX_WARNINGS_DISPLAY]
                for i, warning in enumerate(display_warnings, 1):
                    warning_safe = self._sanitize_html(warning)
                    html_parts.append(f'<div class="warning"><strong>{i}.</strong> {warning_safe}</div>')
                
                if len(self.quality['warnings']) > self.config.MAX_WARNINGS_DISPLAY:
                    remaining = len(self.quality['warnings']) - self.config.MAX_WARNINGS_DISPLAY
                    html_parts.append(
                        f'<div class="warning"><em>... and {remaining} more warnings</em></div>'
                    )
                html_parts.append('</div>')
            
            html_parts.append(f"""
    <div class="card">
        <h2> Column Details (Interactive)</h2>
        
        <div class="controls">
            <button class="btn" onclick="exportTableToCSV()" title="Download visible data as CSV">
                 Download CSV
            </button>
            <button class="btn btn-secondary" onclick="exportToJSON()" title="Download visible data as JSON">
                 Download JSON
            </button>
            <button class="btn btn-secondary" onclick="copyToClipboard()" title="Copy visible data to clipboard">
                 Copy Data
            </button>
            <button class="btn btn-success" onclick="downloadHTMLReport()" title="Download full HTML report">
                 Save Full Report
            </button>
        </div>
        
        <input type="text" 
               class="search-box" 
               id="searchBox" 
               placeholder=" Search columns by name, type, or issues...">
        
        <div class="filter-info" id="filterInfo" style="display: none;">
            <span>Filtering by: <strong id="filterType"></strong></span>
            <button onclick="clearFilter()"> Clear Filter</button>
        </div>
        
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th onclick="sortTable(0)">Column</th>
                        <th onclick="sortTable(1)">Type</th>
                        <th onclick="sortTable(2)">Missing</th>
                        <th onclick="sortTable(3)">Unique</th>
                        <th onclick="sortTable(4)">Issues</th>
                    </tr>
                </thead>
                <tbody id="dataTable">
                    {table_rows_html}
                </tbody>
            </table>
        </div>
    </div>
""")
            
            recommendations = self._generate_recommendations()
            if recommendations:
                html_parts.append('<div class="card"><h2> Actionable Recommendations</h2>')
                for i, rec in enumerate(recommendations, 1):
                    rec_safe = self._sanitize_html(rec)
                    html_parts.append(f'<div class="recommendation"><strong>{i}.</strong> {rec_safe}</div>')
                html_parts.append('</div>')
            
            html_parts.append(f"""
    <div class="card" style="text-align: center; color: #64748b; font-size: 14px;">
        <p>Report generated by <strong>GOAT Data Analyst v2.0</strong></p>
        <p>{self.timestamp}</p>
    </div>
    
    <script>
        {self._get_javascript_code()}
    </script>
</body>
</html>""")
            
            html = ''.join(html_parts)
            logger.info("HTML report generated successfully")
            return html
            
        except Exception as e:
            logger.error(f"Error generating HTML report: {str(e)}", exc_info=True)
            raise
    
    def save_markdown(self, filepath: str) -> None:
        """Save the report as a Markdown file."""
        try:
            md_content = self.generate_markdown()
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(md_content)
            
            logger.info(f"Markdown report saved successfully: {filepath}")
            print(f" Markdown report saved: {filepath}")
            
        except Exception as e:
            logger.error(f"Error saving markdown report: {str(e)}", exc_info=True)
            raise IOError(f"Failed to save markdown report: {str(e)}")
    
    def save_html(self, filepath: str) -> None:
        """Save the report as an HTML file."""
        try:
            html_content = self.generate_html()
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"HTML report saved successfully: {filepath}")
            print(f" HTML report saved: {filepath}")
            
        except Exception as e:
            logger.error(f"Error saving HTML report: {str(e)}", exc_info=True)
            raise IOError(f"Failed to save HTML report: {str(e)}")
    
    def save_both(self, base_filename: str, output_dir: str = 'output') -> Tuple[str, str]:
        """Save both Markdown and HTML versions of the report."""
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            md_path = os.path.join(output_dir, f"{base_filename}.md")
            html_path = os.path.join(output_dir, f"{base_filename}.html")
            
            self.save_markdown(md_path)
            self.save_html(html_path)
            
            logger.info(f"Both reports saved successfully in {output_dir}")
            print(f"\n Reports saved successfully:")
            print(f"    Markdown: {md_path}")
            print(f"    HTML: {html_path}")
            
            return md_path, html_path
            
        except Exception as e:
            logger.error(f"Error saving reports: {str(e)}", exc_info=True)
            raise IOError(f"Failed to save reports: {str(e)}")


