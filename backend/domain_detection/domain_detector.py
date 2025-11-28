"""
Domain Detector - Intelligent Business Domain Classification
Analyzes datasets and identifies their business domain automatically.
"""

import pandas as pd
import re
from typing import Dict, List, Tuple, Optional
from collections import Counter
from backend.domain_detection.patterns import DomainPatterns, DomainPattern


class DomainDetector:
    """
    Production-grade domain detection system.
    Analyzes column names, data patterns, and relationships to identify dataset domain.
    """
    
    def __init__(self):
        """Initialize the domain detector with pattern library."""
        self.patterns = DomainPatterns.get_all_domains()
        self.min_confidence_threshold = 0.15  # Minimum confidence to report
        
    def detect_domain(self, df: pd.DataFrame) -> Dict:
        """
        Detect the business domain of a dataset.
        
        Args:
            df: pandas DataFrame to analyze
            
        Returns:
            Dictionary containing:
            - primary_domain: Most likely domain
            - confidence: Confidence score (0-1)
            - all_scores: Scores for all domains
            - detected_entities: List of domain-specific entities found
            - recommendations: Domain-specific recommendations
        """
        if df is None or df.empty:
            return self._create_empty_result()
        
        # Analyze the dataset
        column_names = [col.lower() for col in df.columns]
        
        # Calculate scores for each domain
        domain_scores = {}
        domain_matches = {}
        
        for pattern in self.patterns:
            score, matches = self._calculate_domain_score(column_names, df, pattern)
            domain_scores[pattern.name] = score
            domain_matches[pattern.name] = matches
        
        # Find primary domain
        if not domain_scores or max(domain_scores.values()) == 0:
            return self._create_empty_result()
        
        primary_domain = max(domain_scores, key=domain_scores.get)
        confidence = domain_scores[primary_domain]
        
        # Get detected entities
        entities = domain_matches[primary_domain]
        
        # Generate recommendations
        recommendations = self._generate_recommendations(primary_domain, entities, df)
        
        # Get secondary domains (confidence > threshold)
        secondary_domains = [
            domain for domain, score in domain_scores.items()
            if domain != primary_domain and score >= self.min_confidence_threshold
        ]
        
        return {
            'primary_domain': primary_domain,
            'confidence': round(confidence, 3),
            'all_scores': {k: round(v, 3) for k, v in domain_scores.items()},
            'detected_entities': entities,
            'secondary_domains': secondary_domains,
            'recommendations': recommendations,
            'column_count': len(df.columns),
            'row_count': len(df)
        }
    
    def _calculate_domain_score(
        self, 
        column_names: List[str], 
        df: pd.DataFrame,
        pattern: DomainPattern
    ) -> Tuple[float, List[str]]:
        """
        Calculate how well a dataset matches a domain pattern.
        
        Returns:
            Tuple of (score, list of matched keywords)
        """
        matches = []
        score = 0.0
        
        # Check each column name against keywords
        for col in column_names:
            # Exact matches
            for keyword in pattern.keywords:
                if keyword in col:
                    matches.append(col)
                    score += 1.0
                    break  # Count each column only once
        
        # Normalize score by number of columns
        if len(column_names) > 0:
            score = score / len(column_names)
        
        # Boost score if we found many matches
        match_ratio = len(matches) / len(column_names) if len(column_names) > 0 else 0
        if match_ratio > 0.5:
            score *= 1.2  # 20% boost for strong matches
        
        # Apply domain weight
        score *= pattern.weight
        
        # Cap at 1.0
        score = min(score, 1.0)
        
        return score, matches
    
    def _generate_recommendations(
        self, 
        domain: str, 
        entities: List[str],
        df: pd.DataFrame
    ) -> List[str]:
        """Generate domain-specific recommendations."""
        recommendations = []
        
        if domain == "e-commerce":
            recommendations.extend([
                "📊 Track conversion rates and cart abandonment",
                "💰 Monitor pricing consistency across products",
                "📦 Analyze shipping times and delivery performance",
                "🔍 Check for duplicate orders or fraudulent transactions",
                "📈 Calculate customer lifetime value (CLV)"
            ])
            
            if any('price' in e for e in entities):
                recommendations.append("💵 Validate all prices are positive and reasonable")
            if any('inventory' in e or 'stock' in e for e in entities):
                recommendations.append("📦 Monitor inventory levels and stock-outs")
                
        elif domain == "finance":
            recommendations.extend([
                "💰 Ensure all transactions balance (debits = credits)",
                "🔒 Check for unusual transaction patterns (fraud detection)",
                "📊 Calculate key financial ratios and metrics",
                "📈 Analyze cash flow trends over time",
                "⚖️ Verify decimal precision for monetary amounts"
            ])
            
            if any('balance' in e for e in entities):
                recommendations.append("💵 Monitor account balances for anomalies")
            if any('transaction' in e for e in entities):
                recommendations.append("🔍 Flag suspicious transaction amounts or patterns")
                
        elif domain == "crm":
            recommendations.extend([
                "📧 Validate email formats and phone numbers",
                "📊 Calculate lead conversion rates by stage",
                "💼 Track deal velocity through pipeline",
                "🎯 Segment customers by behavior and value",
                "📈 Monitor customer churn and retention rates"
            ])
            
            if any('email' in e for e in entities):
                recommendations.append("✉️ Verify email format validity")
            if any('score' in e or 'rating' in e for e in entities):
                recommendations.append("⭐ Analyze score distributions and trends")
                
        elif domain == "healthcare":
            recommendations.extend([
                "🏥 Ensure HIPAA compliance for patient data",
                "💊 Validate medication dosages and interactions",
                "📅 Track appointment no-show rates",
                "🔬 Monitor lab result turnaround times",
                "👨‍⚕️ Analyze patient outcomes by treatment type"
            ])
            
            recommendations.append("⚠️ CRITICAL: Ensure PHI (Protected Health Information) security")
            
        elif domain == "hr":
            recommendations.extend([
                "💰 Analyze salary equity across departments",
                "📊 Calculate employee turnover rates",
                "⏰ Monitor overtime and time-off patterns",
                "📈 Track performance review completion",
                "🎯 Identify skills gaps and training needs"
            ])
            
            if any('salary' in e or 'compensation' in e for e in entities):
                recommendations.append("💵 Check for salary data consistency and fairness")
                
        elif domain == "logistics":
            recommendations.extend([
                "📦 Track on-time delivery rates",
                "🚚 Optimize route efficiency and fuel costs",
                "📊 Monitor warehouse utilization rates",
                "⏱️ Calculate average delivery times by region",
                "📍 Analyze shipping zones and costs"
            ])
            
            if any('tracking' in e for e in entities):
                recommendations.append("🔍 Validate tracking number formats")
                
        elif domain == "marketing":
            recommendations.extend([
                "📊 Calculate ROI by campaign and channel",
                "🎯 Analyze conversion rates by segment",
                "📈 Track engagement metrics over time",
                "💰 Optimize cost per acquisition (CPA)",
                "🔄 Identify high-performing content types"
            ])
            
            if any('click' in e or 'impression' in e for e in entities):
                recommendations.append("📊 Calculate click-through rates (CTR)")
        
        return recommendations
    
    def _create_empty_result(self) -> Dict:
        """Create result structure for datasets with no clear domain."""
        return {
            'primary_domain': 'unknown',
            'confidence': 0.0,
            'all_scores': {},
            'detected_entities': [],
            'secondary_domains': [],
            'recommendations': [
                "❓ Unable to determine domain automatically",
                "💡 This might be a custom or mixed-domain dataset",
                "🔍 Review column names for domain-specific terminology"
            ],
            'column_count': 0,
            'row_count': 0
        }
    
    def get_domain_summary(self, result: Dict) -> str:
        """
        Generate a human-readable summary of domain detection.
        
        Args:
            result: Result dictionary from detect_domain()
            
        Returns:
            Formatted string summary
        """
        if result['primary_domain'] == 'unknown':
            return "⚠️ Domain: Unknown - Unable to classify this dataset"
        
        summary = f"🎯 Primary Domain: {result['primary_domain'].upper()}\n"
        summary += f"📊 Confidence: {result['confidence']:.1%}\n"
        summary += f"📁 Dataset Size: {result['row_count']:,} rows × {result['column_count']} columns\n"
        
        if result['detected_entities']:
            summary += f"\n🔍 Detected Entities ({len(result['detected_entities'])}):\n"
            for entity in result['detected_entities'][:5]:  # Show first 5
                summary += f"   • {entity}\n"
            if len(result['detected_entities']) > 5:
                summary += f"   ... and {len(result['detected_entities']) - 5} more\n"
        
        if result['secondary_domains']:
            summary += f"\n🔄 Secondary Domains: {', '.join(result['secondary_domains'])}\n"
        
        return summary
