# ============================================================================
# AI Engine - Central AI wrapper for GOAT
# ============================================================================
# Handles all LLM interactions (Groq API initially)
# Designed to be model-agnostic - can swap Groq → Claude → GPT easily
# ============================================================================

import os
import json
from typing import Optional, Dict, Any, List
import pandas as pd


class AIEngine:
    """
    Central AI wrapper for GOAT Data Analyst
    
    Handles:
    - Domain detection enhancement
    - Pain point explanation generation
    - Action plan creation
    - Context-aware suggestions
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize AI engine
        
        Args:
            api_key: Groq API key (or use GROQ_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY", "")
        self.model = "llama-3.3-70b-versatile"  # Replacement for mixtral (better performance)
        self.enabled = bool(self.api_key and self.api_key != "your-groq-api-key-here")
        
        if self.enabled:
            try:
                from groq import Groq
                self.client = Groq(api_key=self.api_key)
                print("✓ AIEngine initialized (Groq API)")
            except ImportError:
                print("⚠️  groq package not installed - AI features disabled")
                self.enabled = False
        else:
            self.client = None
            print("⚠️  AIEngine initialized without API key - using rule-based fallbacks")
    
    def detect_domain(
        self, 
        df: pd.DataFrame, 
        profile: Dict,
        rule_based_guess: Dict
    ) -> Dict[str, Any]:
        """
        Enhanced domain detection using AI
        
        Args:
            df: DataFrame to analyze
            profile: Data profile with column info
            rule_based_guess: Initial guess from rule-based detector
        
        Returns:
            {"type": str, "confidence": float, "reasoning": str}
        """
        # If AI disabled or rule-based is confident, use that
        if not self.enabled or rule_based_guess.get("confidence", 0) > 0.8:
            return rule_based_guess
        
        # Build prompt for AI
        column_sample = self._get_column_sample(df, profile)
        
        prompt = f"""Analyze this dataset and identify its domain type.

Column names: {', '.join(df.columns.tolist())}

Sample data (first 3 rows):
{df.head(3).to_dict('records')}

Column types: {column_sample}

Domain options:
- sales: Transaction data with products, prices, dates
- finance: Accounting, budgets, expenses, revenue
- ecommerce: Online store data with customers, orders
- marketing: Campaigns, conversions, metrics
- healthcare: Patient records, medical data
- hr: Employee data, payroll, attendance
- inventory: Stock levels, warehouses, SKUs
- customer: CRM data, interactions, support
- web_analytics: Page views, sessions, user behavior
- logistics: Shipping, deliveries, tracking
- generic: General business data

Rule-based guess: {rule_based_guess.get('type', 'unknown')} (confidence: {rule_based_guess.get('confidence', 0):.2f})

Respond ONLY with JSON:
{{"type": "domain_name", "confidence": 0.0-1.0, "reasoning": "brief explanation"}}"""

        try:
            response = self._call_llm(prompt)
            result = json.loads(response)
            
            # Validate response
            if "type" in result and "confidence" in result:
                return result
            else:
                return rule_based_guess
                
        except Exception as e:
            print(f"⚠️  AI domain detection failed: {e}")
            return rule_based_guess
    
    def explain_pain_points(
        self,
        df: pd.DataFrame,
        quality: Dict,
        profile: Dict,
        domain: Dict
    ) -> List[Dict[str, Any]]:
        """
        Generate human-readable explanations for data quality issues
        
        Args:
            df: DataFrame being analyzed
            quality: Quality metrics (missing, dupes, outliers)
            profile: Data profile
            domain: Domain type for context
        
        Returns:
            List of pain points with severity, explanation, and fix suggestion
            [{"severity": "high", "issue": "...", "impact": "...", "fix": "..."}]
        """
        if not self.enabled:
            return self._rule_based_pain_points(quality, profile)
        
        # Build context
        issues_summary = self._summarize_quality_issues(quality, df)
        
        prompt = f"""You are a data analyst explaining data quality issues to a business user.

Dataset: {domain.get('type', 'unknown')} data
Rows: {len(df)}, Columns: {len(df.columns)}

Quality Issues Detected:
{issues_summary}

Generate a prioritized list of pain points with:
1. Severity (critical/high/medium/low)
2. Clear explanation of the issue
3. Business impact (why it matters)
4. Suggested fix (actionable step)

Respond ONLY with JSON array:
[
  {{
    "severity": "high",
    "issue": "12% of amount column is empty",
    "impact": "Revenue calculations will be incorrect",
    "fix": "Fill missing values with median or flag for manual review"
  }}
]

Focus on the TOP 5 most important issues. Be specific and actionable."""

        try:
            response = self._call_llm(prompt)
            result = json.loads(response)
            
            if isinstance(result, list) and len(result) > 0:
                return result
            else:
                return self._rule_based_pain_points(quality, profile)
                
        except Exception as e:
            print(f"⚠️  AI pain point generation failed: {e}")
            return self._rule_based_pain_points(quality, profile)
    
    def generate_action_plan(
        self,
        domain: Dict,
        pain_points: List[Dict],
        profile: Dict,
        analytics: Dict
    ) -> List[str]:
        """
        Generate sequenced, actionable steps based on pain points
        
        Args:
            domain: Domain type
            pain_points: List of issues from explain_pain_points
            profile: Data profile
            analytics: Statistical analysis results
        
        Returns:
            List of ordered action steps
        """
        if not self.enabled:
            return self._rule_based_action_plan(pain_points)
        
        prompt = f"""Create a step-by-step action plan for fixing this dataset.

Domain: {domain.get('type', 'unknown')}
Issues identified:
{json.dumps(pain_points, indent=2)}

Generate an ordered list of 5-7 specific action steps:
1. Address highest severity issues first
2. Sequence logically (clean before validate before analyze)
3. Be specific (not "fix data" but "remove 47 duplicate rows")
4. Include validation steps

Respond ONLY with JSON array of strings:
["Step 1: Remove 47 duplicate transaction IDs", "Step 2: Fill missing amounts with median", ...]"""

        try:
            response = self._call_llm(prompt)
            result = json.loads(response)
            
            if isinstance(result, list) and len(result) > 0:
                return result
            else:
                return self._rule_based_action_plan(pain_points)
                
        except Exception as e:
            print(f"⚠️  AI action plan failed: {e}")
            return self._rule_based_action_plan(pain_points)
    
    def _call_llm(self, prompt: str, max_tokens: int = 1000) -> str:
        """Call Groq API with prompt"""
        if not self.enabled:
            raise Exception("AI not enabled")
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a data quality analyst. Always respond with valid JSON only, no markdown formatting."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,  # Lower = more consistent
            max_tokens=max_tokens
        )
        
        return response.choices[0].message.content.strip()
    
    def _get_column_sample(self, df: pd.DataFrame, profile: Dict) -> str:
        """Get representative column info"""
        col_info = []
        for col in df.columns[:10]:  # First 10 columns
            dtype = str(df[col].dtype)
            unique = df[col].nunique()
            col_info.append(f"{col} ({dtype}, {unique} unique)")
        return ", ".join(col_info)
    
    def _summarize_quality_issues(self, quality: Dict, df: pd.DataFrame) -> str:
        """Summarize quality issues for AI"""
        lines = []
        
        # Missing data
        missing_pct = quality.get('missing_pct', 0)
        if missing_pct > 0:
            lines.append(f"- Overall missing data: {missing_pct:.1f}%")
            missing_by_col = quality.get('missing_by_column', {})
            top_missing = sorted(missing_by_col.items(), key=lambda x: x[1], reverse=True)[:3]
            for col, count in top_missing:
                if count > 0:
                    pct = (count / len(df)) * 100
                    lines.append(f"  • {col}: {count} missing ({pct:.1f}%)")
        
        # Duplicates
        dupes = quality.get('duplicates', 0)
        if dupes > 0:
            lines.append(f"- Duplicate rows: {dupes} ({dupes/len(df)*100:.1f}%)")
        
        # Outliers (if detected)
        outliers = quality.get('outliers', {})
        if outliers:
            lines.append(f"- Outliers detected in {len(outliers)} columns")
        
        return "\n".join(lines) if lines else "No major issues detected"
    
    def _rule_based_pain_points(self, quality: Dict, profile: Dict) -> List[Dict]:
        """Fallback rule-based pain point generation"""
        pain_points = []
        
        missing_pct = quality.get('missing_pct', 0)
        if missing_pct > 5:
            pain_points.append({
                "severity": "high" if missing_pct > 20 else "medium",
                "issue": f"{missing_pct:.1f}% of data is missing",
                "impact": "Analysis results will be incomplete or biased",
                "fix": "Review missing data patterns and decide on fill strategy"
            })
        
        dupes = quality.get('duplicates', 0)
        if dupes > 0:
            pain_points.append({
                "severity": "high" if dupes > 100 else "medium",
                "issue": f"{dupes} duplicate rows found",
                "impact": "Metrics and counts will be inflated",
                "fix": "Remove duplicates after verifying they are true duplicates"
            })
        
        return pain_points
    
    def _rule_based_action_plan(self, pain_points: List[Dict]) -> List[str]:
        """Fallback rule-based action plan"""
        steps = []
        
        # Sort by severity
        sorted_points = sorted(
            pain_points,
            key=lambda x: {"critical": 4, "high": 3, "medium": 2, "low": 1}.get(x.get("severity", "low"), 1),
            reverse=True
        )
        
        for i, point in enumerate(sorted_points[:5], 1):
            steps.append(f"{i}. {point.get('fix', 'Address: ' + point.get('issue', 'Unknown issue'))}")
        
        return steps


# Test function
def _test():
    """Test AI engine with and without API key"""
    print("\n" + "="*70)
    print("TESTING AI ENGINE")
    print("="*70)
    
    # Test without API key (fallback mode)
    print("\n1. Testing without API key (rule-based fallback):")
    engine = AIEngine()
    print(f"   Enabled: {engine.enabled}")
    
    # Create test data
    df = pd.DataFrame({
        'transaction_id': range(100),
        'amount': [100 if i % 10 != 0 else None for i in range(100)],
        'category': ['A', 'B', 'C'] * 33 + ['A']
    })
    
    quality = {
        'missing_pct': 10.0,
        'duplicates': 5,
        'missing_by_column': {'amount': 10}
    }
    
    profile = {'rows': 100, 'columns': 3}
    
    pain_points = engine.explain_pain_points(df, quality, profile, {"type": "sales"})
    print(f"\n   Pain points generated: {len(pain_points)}")
    for p in pain_points:
        print(f"   - [{p['severity']}] {p['issue']}")
    
    action_plan = engine.generate_action_plan(
        {"type": "sales"},
        pain_points,
        profile,
        {}
    )
    print(f"\n   Action plan steps: {len(action_plan)}")
    for step in action_plan:
        print(f"   {step}")
    
    print("\n" + "="*70)
    print("✅ AI Engine test complete (fallback mode working)")
    print("="*70)


if __name__ == "__main__":
    _test()
