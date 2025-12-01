"""Domain Detection Section - Generates HTML for domain intelligence card."""

from typing import Dict, Any, Optional


class DomainSection:
    """Generates domain detection HTML section."""
    
    def generate(self, domain_data: Dict[str, Any]) -> str:
        """
        Generate domain detection HTML.
        
        Args:
            domain_data: Dict containing:
                - detected_domain: str
                - confidence: float (0-1)
                - key_entities: list of str
                - top_domains: list of tuples (domain, score) - optional
        
        Returns:
            HTML string for domain section
        """
        if not domain_data or not domain_data.get("detected_domain"):
            return ""
        
        domain = domain_data["detected_domain"]
        confidence = domain_data.get("confidence", 0) * 100  # Convert to percentage
        entities = domain_data.get("key_entities", [])
        top_domains = domain_data.get("top_domains", [])
        
        html = f"""
        <div class="card">
            <div class="card-header">
                <h2>🎯 Domain Intelligence</h2>
            </div>
            <div class="card-body">
                <div class="metric-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                    <div class="metric-label">Detected Domain</div>
                    <div class="metric-value" style="font-size: 2rem; color: white;">{domain.upper()}</div>
                    <div class="metric-label">Confidence: {confidence:.1f}%</div>
                    <p style="color: rgba(255,255,255,0.9); margin-top: 1rem; font-size: 0.9rem;">
                        This is a best guess based on column names and data patterns. 
                        Use as orientation, not absolute truth.
                    </p>
                </div>
        """
        
        # Add top domain candidates if available
        if top_domains and len(top_domains) > 1:
            html += """
                <div style="margin-top: 1.5rem;">
                    <h3 style="font-size: 1.1rem; margin-bottom: 1rem;">Alternative Domains</h3>
            """
            
            for alt_domain, score in top_domains[1:4]:  # Top 3 alternatives
                bar_width = (score / top_domains[0][1] * 100) if top_domains[0][1] > 0 else 0
                html += f"""
                    <div style="margin-bottom: 0.8rem;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem;">
                            <span style="font-weight: 500;">{alt_domain}</span>
                            <span style="color: #666;">{score:.1f}</span>
                        </div>
                        <div style="background: #f0f0f0; height: 8px; border-radius: 4px; overflow: hidden;">
                            <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                                        height: 100%; width: {bar_width}%; transition: width 0.3s;">
                            </div>
                        </div>
                    </div>
                """
            
            html += "</div>"
        
        # Add key entities
        if entities:
            html += """
                <div style="margin-top: 1.5rem;">
                    <h3 style="font-size: 1.1rem; margin-bottom: 1rem;">Key Entities</h3>
                    <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
            """
            
            for entity in entities[:10]:  # Limit to 10 entities
                html += f"""
                    <span style="background: #f0f0f0; padding: 0.4rem 0.8rem; 
                                border-radius: 20px; font-size: 0.9rem; color: #333;">
                        {entity}
                    </span>
                """
            
            html += "</div></div>"
        
        html += """
            </div>
        </div>
        """
        
        return html
