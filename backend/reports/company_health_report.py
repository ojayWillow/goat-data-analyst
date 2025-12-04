"""
Company Health Report Generator

Day 16: Turn BatchEngine output into an executive-friendly HTML report.

Input:
- batch_result: {
    'files': [AnalysisResult, ...],
    'summary': {
        'total_files': int,
        'total_rows': int,
        'avg_quality_score': float,
        'total_issues': int,
        'files_needing_attention': [ { filename, quality_score, issues }, ... ],
        'top_issues': [ { type, severity, count, description }, ... ]
    }
}

Output:
- HTML string with:
    - Overall health score
    - Key issues
    - Prioritized files
    - File-by-file summary table
"""

from typing import Dict, List
import datetime
import html


class CompanyHealthReportGenerator:
    """Generate an HTML company health report from batch analysis results."""

    def generate(self, batch_result: Dict) -> str:
        summary = batch_result.get('summary', {})
        files = batch_result.get('files', [])

        total_files = summary.get('total_files', 0)
        total_rows = summary.get('total_rows', 0)
        avg_quality_score = summary.get('avg_quality_score', 0.0)
        total_issues = summary.get('total_issues', 0)
        files_needing_attention = summary.get('files_needing_attention', [])
        top_issues = summary.get('top_issues', [])

        generated_at = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

        html_parts: List[str] = []

        html_parts.append("""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>Company Data Health Report</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 0; padding: 0; background: #0f172a; color: #e5e7eb; }
        .container { max-width: 1100px; margin: 0 auto; padding: 32px 24px 64px 24px; }
        h1, h2, h3, h4 { color: #f9fafb; margin-bottom: 8px; }
        .pill { display: inline-block; padding: 2px 10px; border-radius: 999px; font-size: 12px; border: 1px solid rgba(148, 163, 184, 0.5); color: #e5e7eb; }
        .section { margin-top: 32px; padding: 20px; border-radius: 16px; background: #020617; border: 1px solid rgba(148, 163, 184, 0.35); box-shadow: 0 18px 45px rgba(15, 23, 42, 0.9); }
        .muted { color: #9ca3af; font-size: 14px; }
        .metric-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px; margin-top: 16px; }
        .metric { padding: 16px 14px; border-radius: 14px; background: linear-gradient(135deg, rgba(15,23,42,0.95), rgba(30,64,175,0.25)); border: 1px solid rgba(129, 140, 248, 0.35); }
        .metric-label { font-size: 12px; text-transform: uppercase; letter-spacing: 0.08em; color: #9ca3af; margin-bottom: 4px; }
        .metric-value { font-size: 22px; font-weight: 600; margin-bottom: 2px; }
        .metric-hint { font-size: 12px; color: #9ca3af; }
        .badge-green { color: #22c55e; }
        .badge-amber { color: #f97316; }
        .badge-red { color: #ef4444; }
        .tag { display: inline-block; padding: 3px 10px; border-radius: 999px; font-size: 11px; background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(148, 163, 184, 0.6); margin-right: 6px; margin-bottom: 6px; }
        .tag-high { border-color: rgba(239, 68, 68, 0.7); color: #fecaca; }
        .tag-medium { border-color: rgba(245, 158, 11, 0.7); color: #fed7aa; }
        .tag-low { border-color: rgba(34, 197, 94, 0.6); color: #bbf7d0; }
        .issue-item { margin-bottom: 10px; padding: 8px 10px; border-radius: 10px; background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(107, 114, 128, 0.6); }
        .issue-title { font-size: 14px; font-weight: 500; margin-bottom: 2px; }
        .issue-meta { font-size: 12px; color: #9ca3af; }
        table { width: 100%; border-collapse: collapse; margin-top: 12px; font-size: 13px; }
        th, td { text-align: left; padding: 8px 8px; border-bottom: 1px solid rgba(55, 65, 81, 0.9); }
        th { font-size: 12px; text-transform: uppercase; letter-spacing: 0.08em; color: #9ca3af; background: rgba(15, 23, 42, 0.95); }
        tr:nth-child(even) td { background: rgba(15, 23, 42, 0.75); }
        .chip { display: inline-flex; align-items: center; padding: 2px 8px; border-radius: 999px; font-size: 11px; }
        .chip-red { background: rgba(127, 29, 29, 0.9); color: #fecaca; }
        .chip-amber { background: rgba(120, 53, 15, 0.9); color: #fed7aa; }
        .chip-green { background: rgba(20, 83, 45, 0.9); color: #bbf7d0; }
        .file-name { font-weight: 500; }
        .section-title-row { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 6px; }
        .section-title-row h2 { margin: 0; }
        .section-title-row span { font-size: 13px; color: #9ca3af; }
        .plan-item { margin-bottom: 8px; padding: 8px 10px; border-radius: 10px; background: rgba(15,23,42,0.9); border: 1px dashed rgba(148, 163, 184, 0.7); }
        .plan-label { font-size: 12px; text-transform: uppercase; letter-spacing: 0.08em; color: #9ca3af; margin-bottom: 2px; }
        .plan-body { font-size: 13px; color: #e5e7eb; }
        .hl { color: #e5e7eb; font-weight: 500; }
    </style>
</head>
<body>
    <div class="container">
""")

        # Header
        html_parts.append(f"""
        <div class="section" style="margin-top: 0; background: radial-gradient(circle at top left, rgba(56,189,248,0.25), transparent 55%), radial-gradient(circle at top right, rgba(129,140,248,0.25), transparent 55%), #020617;">
            <span class="pill">Executive Overview · Company Data Health</span>
            <h1 style="margin-top: 10px; font-size: 28px;">Company Data Health Report</h1>
            <p class="muted" style="max-width: 640px;">
                This report summarizes data quality across all analyzed files. It highlights systemic risks,
                prioritizes which datasets require attention, and provides a focused action plan for your team.
            </p>
            <p class="muted" style="font-size: 12px; margin-top: 10px;">Generated: {html.escape(generated_at)}</p>
        </div>
""")

        # Overall metrics
        score_badge_class = "badge-red" if avg_quality_score < 60 else "badge-amber" if avg_quality_score < 80 else "badge-green"
        score_label = "Critical" if avg_quality_score < 60 else "At Risk" if avg_quality_score < 80 else "Healthy"

        files_needing_count = len(files_needing_attention)

        html_parts.append("""
        <div class="section">
            <div class="section-title-row">
                <h2>Overall Data Health</h2>
                <span>High-level view of all analyzed files</span>
            </div>
            <div class="metric-grid">
        """)

        html_parts.append(f"""
                <div class="metric">
                    <div class="metric-label">Avg. Data Quality Score</div>
                    <div class="metric-value"><span class="{score_badge_class}">{avg_quality_score:.0f}/100</span></div>
                    <div class="metric-hint">{score_label} across all analyzed files</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Files Analyzed</div>
                    <div class="metric-value">{total_files}</div>
                    <div class="metric-hint">Covering all uploaded datasets</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Total Rows</div>
                    <div class="metric-value">{total_rows:,}</div>
                    <div class="metric-hint">Combined volume across all files</div>
                </div>
                <div class="metric">
                    <div class="metric-label">Files Needing Attention</div>
                    <div class="metric-value">{files_needing_count}</div>
                    <div class="metric-hint">Below recommended quality threshold</div>
                </div>
            </div>
        </div>
""")

        # Top issues section
        html_parts.append("""
        <div class="section">
            <div class="section-title-row">
                <h2>Systemic Data Quality Issues</h2>
                <span>Patterns that appear across multiple files</span>
            </div>
        """)

        if not top_issues:
            html_parts.append("""
            <p class="muted">No systemic issues detected across your datasets. Maintain current collection and validation processes.</p>
        """)
        else:
            for issue in top_issues:
                severity = issue.get('severity', 'medium')
                description = issue.get('description', 'Issue')
                count = issue.get('count', 0)
                issue_type = issue.get('type', '')

                if severity == 'high':
                    badge = "🔴 High impact"
                    tag_class = "tag-high"
                elif severity == 'medium':
                    badge = "🟡 Moderate"
                    tag_class = "tag-medium"
                else:
                    badge = "🟢 Low"
                    tag_class = "tag-low"

                html_parts.append(f"""
            <div class="issue-item">
                <div class="issue-title">{html.escape(description)}</div>
                <div class="issue-meta">
                    <span class="tag {tag_class}">{badge}</span>
                    <span class="tag">Seen in {count} file(s)</span>
                    <span class="tag">Category: {html.escape(issue_type)}</span>
                </div>
            </div>
        """)

            html_parts.append("""
            <p class="muted" style="margin-top: 8px;">
                These are the most common patterns driving down your overall data quality score.
                Tackling them will improve multiple datasets at once.
            </p>
        """)

        html_parts.append("</div>")

        # Prioritized action plan
        html_parts.append("""
        <div class="section">
            <div class="section-title-row">
                <h2>Prioritized Action Plan</h2>
                <span>What to fix first to get the biggest impact</span>
            </div>
        """)

        # Build a simple action plan based on the issues we see
        if files_needing_attention:
            # 1. Top risk files
            top_files_names = ", ".join(html.escape(f["filename"]) for f in files_needing_attention[:3])
            html_parts.append(f"""
            <div class="plan-item">
                <div class="plan-label">Step 1 · Stabilize highest-risk datasets</div>
                <div class="plan-body">
                    Focus first on <span class="hl">{top_files_names}</span>. These files have the lowest
                    quality scores and are likely to introduce the most noise into downstream reporting.
                    Resolve missing data, duplicates, and date inconsistencies here before touching smaller issues.
                </div>
            </div>
            """)

        # 2. Issue-type based actions
        issue_types = {i["type"]: i for i in top_issues} if top_issues else {}

        if "missing_data" in issue_types:
            html_parts.append("""
            <div class="plan-item">
                <div class="plan-label">Step 2 · Implement robust missing data strategy</div>
                <div class="plan-body">
                    Missing values are appearing across multiple datasets. Standardize your approach by:
                    defining default imputation rules for key metrics, enforcing required fields at data entry,
                    and monitoring new missingness over time. Align business stakeholders on when imputation is
                    acceptable versus when data must be recollected.
                </div>
            </div>
            """)

        if "duplicates" in issue_types:
            html_parts.append("""
            <div class="plan-item">
                <div class="plan-label">Step 3 · Eliminate duplicate records at the source</div>
                <div class="plan-body">
                    Duplicate rows are impacting multiple files. Introduce de-duplication logic at ingestion,
                    define clear primary keys for each dataset, and add validation checks to prevent repeated
                    uploads or double-counted transactions.
                </div>
            </div>
            """)

        if "date_formats" in issue_types:
            html_parts.append("""
            <div class="plan-item">
                <div class="plan-label">Step 4 · Standardize date formats</div>
                <div class="plan-body">
                    Inconsistent date formats create silent reporting errors. Move towards a single canonical
                    format (e.g. ISO <span class="hl">YYYY-MM-DD</span>) in storage, and apply conversion logic
                    at ingestion so analysts do not need to manually normalize dates per file.
                </div>
            </div>
            """)

        if "outliers" in issue_types:
            html_parts.append("""
            <div class="plan-item">
                <div class="plan-label">Step 5 · Define clear outlier policies</div>
                <div class="plan-body">
                    Outliers in numeric fields should be governed by business rules rather than ad-hoc filtering.
                    Work with domain owners to define what constitutes an impossible or implausible value, and
                    encode these rules into validation checks or automated cleaning steps.
                </div>
            </div>
            """)

        if "capitalization" in issue_types:
            html_parts.append("""
            <div class="plan-item">
                <div class="plan-label">Step 6 · Enforce consistent categorical labels</div>
                <div class="plan-body">
                    Mixed capitalization and inconsistent labels make grouping and segmentation difficult.
                    Introduce standardized vocabularies for key dimensions (e.g. product category, region)
                    and ensure all ingestion pipelines normalize text fields to an agreed casing convention.
                </div>
            </div>
            """)

        if not top_issues and not files_needing_attention:
            html_parts.append("""
            <p class="muted">
                No major cross-file issues detected. Focus on incremental improvements, documentation,
                and monitoring rather than large remediation projects.
            </p>
            """)

        html_parts.append("</div>")

        # File-by-file summary table
        html_parts.append("""
        <div class="section">
            <div class="section-title-row">
                <h2>File-by-File Summary</h2>
                <span>Quality scores and key issues per dataset</span>
            </div>
        """)

        if not files:
            html_parts.append("<p class=\"muted\">No files in batch result.</p>")
        else:
            html_parts.append("""
            <table>
                <thead>
                    <tr>
                        <th style="width: 34%;">File</th>
                        <th style="width: 12%;">Quality</th>
                        <th style="width: 12%;">Rows</th>
                        <th>Key Issues</th>
                    </tr>
                </thead>
                <tbody>
            """)

            for r in files:
                filename = getattr(r, "filename", "Unknown file")
                q = r.quality or {}
                p = r.profile or {}

                score = q.get("overall_score", 0)
                rows = p.get("rows", p.get("overall", {}).get("rows", 0))

                if score >= 80:
                    chip_class = "chip-green"
                    chip_text = "Healthy"
                elif score >= 60:
                    chip_class = "chip-amber"
                    chip_text = "At risk"
                else:
                    chip_class = "chip-red"
                    chip_text = "Critical"

                # Reuse summarization logic similar to BatchEngine._summarize_issues
                issues_list = []
                missing_pct = q.get("missing_pct", 0)
                if missing_pct > 5:
                    issues_list.append(f"Missing data {missing_pct:.1f}%")
                duplicates = q.get("duplicates", 0)
                if duplicates > 0:
                    issues_list.append(f"{duplicates} duplicates")
                outliers = q.get("outliers", {})
                if outliers:
                    issues_list.append(f"Outliers in {len(outliers)} column(s)")
                date_issues = q.get("date_format_issues", {})
                if date_issues:
                    issues_list.append("Date format issues")
                cap_issues = q.get("capitalization_issues", {})
                if cap_issues:
                    issues_list.append("Capitalization inconsistencies")

                if not issues_list and not r.errors:
                    issues_str = "No major issues"
                elif r.errors:
                    issues_str = "Error during analysis"
                else:
                    issues_str = " · ".join(issues_list)

                html_parts.append(f"""
                    <tr>
                        <td class="file-name">{html.escape(filename)}</td>
                        <td>
                            <span class="chip {chip_class}">{score:.0f}/100 · {chip_text}</span>
                        </td>
                        <td>{rows:,}</td>
                        <td>{html.escape(issues_str)}</td>
                    </tr>
                """)

            html_parts.append("""
                </tbody>
            </table>
        """)

        html_parts.append("</div>")  # end file summary section

        # Footer
        html_parts.append("""
        <div style="margin-top: 24px; text-align: right;">
            <p class="muted" style="font-size: 11px;">
                Generated by GOAT Data Analyst · Company Data Health Module
            </p>
        </div>
    </div>
</body>
</html>
""")

        return "".join(html_parts)
