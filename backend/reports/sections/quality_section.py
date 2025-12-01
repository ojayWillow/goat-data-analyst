"""Quality Report Section - Generates HTML for data quality checks."""

from typing import Dict, Any


class QualitySection:
    """Generates data quality HTML section."""
    
    def generate(self, profile: Dict[str, Any]) -> str:
        """
        Generate quality checks HTML.
        
        Args:
            profile: Dict containing data quality metrics:
                - quality_score: float (0-100)
                - total_rows: int
                - total_columns: int
                - missing_data_pct: float
                - duplicate_rows: int
                - issues: list of str
        
        Returns:
            HTML string for quality section
        """
        if not profile:
            return ""
        
        score = profile.get("quality_score", 0)
        missing = profile.get("missing_data_pct", 0)
        duplicates = profile.get("duplicate_rows", 0)
        issues = profile.get("issues", [])
        
        # Color based on score
        if score >= 80:
            color = "#10b981"
            status = "Excellent"
        elif score >= 60:
            color = "#f59e0b"
            status = "Good"
        else:
            color = "#ef4444"
            status = "Needs Attention"
        
        html = f"""
        <div class="card">
            <div class="card-header">
                <h2>🔍 Data Quality Report</h2>
            </div>
            <div class="card-body">
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 20px;">
                    <div style="background: linear-gradient(135deg, {color} 0%, {color}dd 100%); padding: 16px; border-radius: 8px; color: white;">
                        <div style="font-size: 12px; opacity: 0.9;">Quality Score</div>
                        <div style="font-size: 28px; font-weight: bold;">{score}/100</div>
                        <div style="font-size: 12px; opacity: 0.9;">{status}</div>
                    </div>
                    
                    <div style="background: #f3f4f6; padding: 16px; border-radius: 8px;">
                        <div style="font-size: 12px; color: #666;">Missing Data</div>
                        <div style="font-size: 20px; font-weight: bold; color: #333;">{missing:.1f}%</div>
                    </div>
                    
                    <div style="background: #f3f4f6; padding: 16px; border-radius: 8px;">
                        <div style="font-size: 12px; color: #666;">Duplicate Rows</div>
                        <div style="font-size: 20px; font-weight: bold; color: #333;">{duplicates}</div>
                    </div>
                </div>
        """
        
        # Add issues if any
        if issues:
            html += """
                <div style="margin-top: 20px;">
                    <h3 style="font-size: 1rem; margin-bottom: 12px;">⚠️ Issues Found</h3>
                    <ul style="padding-left: 20px; line-height: 1.8;">
            """
            
            for issue in issues[:10]:  # Limit to 10 issues
                html += f"<li style='color: #666; margin-bottom: 8px;'>{issue}</li>"
            
            html += """
                    </ul>
                </div>
            """
        else:
            html += """
                <div style="margin-top: 20px; padding: 12px; background: #ecfdf5; border-left: 4px solid #10b981; border-radius: 4px;">
                    <p style="color: #059669; font-weight: 500;">✅ No major quality issues detected!</p>
                </div>
            """
        
        html += """
            </div>
        </div>
        """
        
        return html
