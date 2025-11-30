"""
AI-Enhanced Domain Detection
Combines keyword matching with Groq AI for higher accuracy
"""
import json
from groq import Groq
import os
import pandas as pd
from typing import Dict, Any


class AIDomainDetector:
    def __init__(self):
        self.groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))
    
    def enhance_detection(self, df: pd.DataFrame, keyword_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Use AI to validate and enhance keyword-based domain detection.
        
        Args:
            df: DataFrame to analyze
            keyword_result: Result from keyword-based detection
        
        Returns:
            Enhanced domain detection result
        """
        try:
            # Prepare context for AI
            columns = list(df.columns)[:20]  # First 20 columns
            sample_data = df.head(3).to_dict('records')
            
            # Build prompt
            prompt = self._build_prompt(columns, sample_data, keyword_result)
            
            # Call Groq AI
            response = self.groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a business data analyst expert. Analyze datasets and identify their business domain with high accuracy."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,
                max_tokens=500
            )
            
            # Parse AI response
            ai_result = self._parse_ai_response(response.choices[0].message.content)
            
            # Combine keyword + AI results
            final_result = self._combine_results(keyword_result, ai_result)
            
            return final_result
            
        except Exception as e:
            print(f"AI domain detection failed: {e}")
            # Fallback to keyword result
            return keyword_result
    
    def _build_prompt(self, columns: list, sample_data: list, keyword_result: Dict) -> str:
        """Build AI prompt for domain detection."""
        prompt = f"""
Analyze this dataset and determine its business domain.

**Dataset Information:**
Columns: {', '.join(columns)}

Sample rows:
{json.dumps(sample_data, indent=2, default=str)[:500]}...

**Keyword Analysis:**
Suggested domain: {keyword_result.get('primary_domain', 'unknown')}
Confidence: {keyword_result.get('confidence', 0):.1f}%

**Your Task:**
1. Analyze the column names and sample data
2. Determine the most likely business domain
3. Provide confidence score (0-100%)

**Available Domains:**
- e-commerce (online retail, orders, products, customers)
- finance (transactions, accounts, payments, investments)
- healthcare (patients, treatments, appointments, medical)
- marketing (campaigns, leads, conversions, analytics)
- operations (inventory, logistics, supply chain, resources)
- hr (employees, departments, payroll, recruitment)
- media (content, engagement, views, subscribers)

**Response Format (JSON only):**
{{
    "domain": "domain_name",
    "confidence": 95,
    "reasoning": "Brief explanation why this domain fits best"
}}
"""
        return prompt
    
    def _parse_ai_response(self, response_text: str) -> Dict[str, Any]:
        """Parse AI response into structured format."""
        try:
            # Extract JSON from response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            json_str = response_text[json_start:json_end]
            
            result = json.loads(json_str)
            
            return {
                'domain': result.get('domain', 'unknown'),
                'confidence': float(result.get('confidence', 0)),
                'reasoning': result.get('reasoning', '')
            }
        except Exception as e:
            print(f"Failed to parse AI response: {e}")
            return {
                'domain': 'unknown',
                'confidence': 0,
                'reasoning': 'Parse error'
            }
    
    def _combine_results(self, keyword_result: Dict, ai_result: Dict) -> Dict[str, Any]:
        """
        Combine keyword and AI results for final detection.
        AI takes precedence if confidence > keyword confidence.
        """
        keyword_confidence = keyword_result.get('confidence', 0)
        ai_confidence = ai_result.get('confidence', 0)
        
        # Use AI result if confidence is higher
        if ai_confidence > keyword_confidence:
            return {
                'primary_domain': ai_result['domain'],
                'confidence': ai_confidence,
                'method': 'ai_enhanced',
                'ai_reasoning': ai_result['reasoning'],
                'keyword_suggestion': keyword_result.get('primary_domain'),
                'keyword_confidence': keyword_confidence
            }
        else:
            # Keep keyword result but add AI context
            return {
                'primary_domain': keyword_result.get('primary_domain'),
                'confidence': keyword_confidence,
                'method': 'keyword_validated',
                'ai_opinion': ai_result['domain'],
                'ai_confidence': ai_confidence,
                'ai_reasoning': ai_result['reasoning']
            }
