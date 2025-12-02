"""
AI-Powered Insights Engine using Groq
Generates natural language insights and recommendations
"""

import os
import pandas as pd
from typing import List, Dict, Any
from groq import Groq
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


class AIInsightsEngine:
    """Generate AI-powered insights using Groq."""
    
    def __init__(self):
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        self.client = Groq(api_key=api_key)
    
    def generate_insights(
        self, 
        df: pd.DataFrame, 
        domain: str = None,
        analytics_summary: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Generate AI insights from dataset."""
        
        # Prepare dataset summary for AI
        dataset_info = self._prepare_dataset_summary(df, domain, analytics_summary)
        
        # Generate insights
        insights = self._call_groq(dataset_info)
        
        return {
            'ai_insights': insights,
            'domain': domain,
            'generated_at': pd.Timestamp.now().isoformat()
        }
    
    def _prepare_dataset_summary(
        self, 
        df: pd.DataFrame, 
        domain: str,
        analytics_summary: Dict[str, Any]
    ) -> str:
        """Prepare concise dataset summary for AI."""
        
        summary_parts = [
            f"Dataset Analysis for {domain or 'Unknown'} Domain",
            f"\nDataset Size: {len(df):,} rows, {len(df.columns)} columns",
            f"\nColumns: {', '.join(df.columns.tolist()[:10])}" + ("..." if len(df.columns) > 10 else "")
        ]
        
        # Add numeric column stats
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            summary_parts.append(f"\n\nNumeric Columns ({len(numeric_cols)}):")
            for col in numeric_cols[:5]:
                summary_parts.append(
                    f"- {col}: min={df[col].min():.2f}, max={df[col].max():.2f}, "
                    f"mean={df[col].mean():.2f}"
                )
        
        # Add categorical column info
        cat_cols = df.select_dtypes(include=['object', 'category']).columns
        if len(cat_cols) > 0:
            summary_parts.append(f"\n\nCategorical Columns ({len(cat_cols)}):")
            for col in cat_cols[:5]:
                unique_count = df[col].nunique()
                top_value = df[col].mode()[0] if not df[col].mode().empty else "N/A"
                summary_parts.append(f"- {col}: {unique_count} unique values, most common: {top_value}")
        
        # Add analytics summary if provided
        if analytics_summary:
            if 'revenue_trends' in analytics_summary:
                rev = analytics_summary['revenue_trends']
                if rev and 'growth_rate' in rev:
                    summary_parts.append(f"\n\nRevenue Growth Rate: {rev['growth_rate']:.2f}%")
                if rev and 'total_revenue' in rev:
                    summary_parts.append(f"Total Revenue: ${rev['total_revenue']:,.2f}")
        
        # Data quality
        missing_pct = (df.isna().sum().sum() / (len(df) * len(df.columns))) * 100
        summary_parts.append(f"\n\nData Quality: {missing_pct:.1f}% missing data")
        
        return "\n".join(summary_parts)
    
    def _call_groq(self, dataset_info: str) -> List[str]:
        """Call Groq API to generate insights."""
        
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a Senior Data Analyst at a top-tier consulting firm.
Your goal is to find the "So What?" in the data - not just describe it, but explain what it means.

Generate 5-7 high-impact insights. Focus on:
1. ⚠️ Anomalies & Outliers - What looks wrong or unusual?
2. 📈 Key Trends - What is moving significantly?
3. 🔗 Correlations - What affects what?
4. 💡 Business Implications - Why does this matter?
5. ⚡ Quick Wins - What could be fixed immediately?

Guidelines:
- Be concise and specific. No fluff or obvious statements.
- Use business language, not data science jargon.
- Prioritize insights by potential business impact.
- If data quality is poor, flag it as a risk.
- Format as a numbered list (1. 2. 3. etc.)"""
                    },
                    {
                        "role": "user",
                        "content": dataset_info
                    }
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            # Parse response into list
            insights_text = response.choices[0].message.content
            insights = [
                line.strip() 
                for line in insights_text.split('\n') 
                if line.strip() and any(line.strip().startswith(str(i)) for i in range(1, 10))
            ]
            
            return insights if insights else [insights_text]
        
        except Exception as e:
            return [f"AI Insights generation failed: {str(e)}"]
    
    def generate_recommendations(
        self, 
        insights: List[str], 
        domain: str
    ) -> List[str]:
        """Generate specific recommendations based on insights."""
        
        try:
            insights_text = "\n".join(insights)
            
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": f"""You are a senior {domain} business consultant.
Based on the data insights provided, generate 3-5 specific, actionable recommendations.

Each recommendation must:
1. Be concrete and implementable (not vague)
2. Have clear expected outcomes
3. Be prioritized by business impact (most important first)
4. Include rough effort/timeline if relevant

Format as a numbered list (1. 2. 3. etc.).
Be direct and consultant-like - assume the reader knows their business."""
                    },
                    {
                        "role": "user",
                        "content": f"Insights from analysis:\n{insights_text}\n\nProvide specific recommendations:"
                    }
                ],
                temperature=0.7,
                max_tokens=400
            )
            
            recommendations_text = response.choices[0].message.content
            recommendations = [
                line.strip() 
                for line in recommendations_text.split('\n') 
                if line.strip() and any(line.strip().startswith(str(i)) for i in range(1, 10))
            ]
            
            return recommendations if recommendations else [recommendations_text]
        
        except Exception as e:
            return [f"Recommendations generation failed: {str(e)}"]
