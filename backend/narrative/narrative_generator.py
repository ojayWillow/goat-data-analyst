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
        
        Example output:
            "Hi—I can see you're working with sales transaction data from an 
            e-commerce system. You have 12,450 rows across 8 columns, with 
            timestamps spanning January 2023 to December 2024."
        """
        # Placeholder for Day 6
        rows = profile.get('rows', 0)
        cols = profile.get('columns', 0)
        domain_type = domain.get('type', 'unknown')
        
        return f"""
        <div class="narrative-section context">
            <h3>📊 I See You</h3>
            <p>
                Hi—I can see you're working with <strong>{domain_type}</strong> data. 
                You have <strong>{rows:,}</strong> rows across <strong>{cols}</strong> columns.
            </p>
            <p class="placeholder">
                🚧 <em>Full context recognition coming in Day 7</em>
            </p>
        </div>
        """
    
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
        
        Example output:
            "Here's what needs attention:
            1. Missing values: 12% of your 'amount' column is empty—this will break totals.
            2. Duplicates: 47 duplicate transaction IDs found.
            3. Outliers: 3 extreme values in 'price' (99999) look like data entry errors."
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
        
        Example output:
            "Your Path Forward:
            1. Clean: Remove 47 duplicate rows.
            2. Fix: Fill missing 'amount' values with median.
            3. Validate: Check for negative prices (found 2).
            4. Analyze: Segment customers by purchase frequency.
            5. Visualize: Build revenue trend by month."
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
    """Test narrative generator with dummy data"""
    gen = NarrativeGenerator()
    
    # Dummy inputs
    domain = {"type": "sales", "confidence": 0.85}
    profile = {"rows": 5000, "columns": 8, "memory_mb": 2.5}
    quality = {"missing_pct": 12.5, "duplicates": 47, "overall_score": 67}
    analytics = {}
    
    # Generate narratives
    print("\n" + "="*50)
    print("TESTING NARRATIVE GENERATOR")
    print("="*50)
    
    print("\n1. Context:")
    print(gen.generate_context(domain, profile))
    
    print("\n2. Pain Points:")
    print(gen.generate_pain_points(quality, profile))
    
    print("\n3. Action Plan:")
    print(gen.generate_action_plan(domain, quality, analytics, profile))
    
    print("\n4. Full Narrative:")
    print(gen.generate_full_narrative(domain, profile, quality, analytics))
    
    print("\n" + "="*50)
    print("✅ All methods exist and return strings")
    print("="*50)


if __name__ == "__main__":
    _test()
