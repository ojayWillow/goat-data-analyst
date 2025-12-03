import re
from typing import Dict, List

import pandas as pd


class DomainDetector:
    """
    Simple rule-based domain detector with optional AI hook.
    For now we rely only on column-name and value heuristics.
    """

    def __init__(self, ai_engine=None):
        self.ai_engine = ai_engine

    def detect(self, df: pd.DataFrame) -> Dict:
        """
        Return a dict: {"type": <domain>, "confidence": <0-1>}
        """
        # First try rule-based detection
        rule_domain = self._rule_based_detect(df)

        # If we already have a confident rule-based domain, return it
        if rule_domain["confidence"] >= 0.7 or self.ai_engine is None:
            return rule_domain

        # Otherwise, optionally ask AI for refinement (not active now since no API key)
        try:
            ai_domain = self.ai_engine.detect_domain(df, rule_domain)
            # If AI boosts confidence, use it
            if ai_domain and ai_domain.get("confidence", 0) > rule_domain["confidence"]:
                return ai_domain
        except Exception:
            # If AI fails, ignore and fall back to rules
            pass

        return rule_domain

    def _rule_based_detect(self, df: pd.DataFrame) -> Dict:
        col_names = [c.lower() for c in df.columns]

        # Score by domain type
        scores = {
            "sales": 0,
            "finance": 0,
            "ecommerce": 0,
            "marketing": 0,
            "healthcare": 0,
            "hr": 0,
            "inventory": 0,
            "customer": 0,
            "web_analytics": 0,
            "logistics": 0,
        }

        # Helper to increase scores when any of these substrings appear in column names
        def boost(domains: List[str], weight: float = 1.0):
            for d in domains:
                scores[d] += weight

        # Common patterns
        for name in col_names:
            # Sales / Revenue
            if any(k in name for k in ["sales", "revenue", "amount", "order_id", "invoice"]):
                boost(["sales"], 1.5)
            if any(k in name for k in ["price", "discount", "discounted_price", "actual_price"]):
                boost(["sales", "ecommerce"], 1.5)

            # Finance
            if any(k in name for k in ["balance", "asset", "liability", "equity", "interest", "loan"]):
                boost(["finance"], 1.5)

            # Ecommerce / Product catalog / Reviews
            if any(k in name for k in ["product_id", "product_name", "sku", "asin", "item_id"]):
                boost(["ecommerce", "inventory"], 2.0)
            if any(k in name for k in ["review", "rating", "rating_count", "feedback"]):
                boost(["ecommerce", "marketing"], 2.0)
            if any(k in name for k in ["user_id", "user_name", "customer_id"]):
                boost(["ecommerce", "customer"], 1.5)
            if any(k in name for k in ["product_link", "img_link", "url"]):
                boost(["ecommerce", "web_analytics"], 1.0)
            if any(k in name for k in ["category", "subcategory"]):
                boost(["ecommerce", "inventory"], 1.0)

            # Marketing
            if any(k in name for k in ["campaign", "utm_", "clicks", "impressions", "ctr"]):
                boost(["marketing", "web_analytics"], 1.5)

            # Healthcare
            if any(k in name for k in ["patient", "diagnosis", "treatment", "icd"]):
                boost(["healthcare"], 2.0)

            # HR
            if any(k in name for k in ["employee", "emp_id", "salary", "hire_date", "termination"]):
                boost(["hr"], 2.0)

            # Inventory / Logistics
            if any(k in name for k in ["stock", "inventory", "warehouse", "location"]):
                boost(["inventory", "logistics"], 1.5)
            if any(k in name for k in ["shipment", "delivery", "tracking", "carrier"]):
                boost(["logistics"], 2.0)

            # Web analytics
            if any(k in name for k in ["session", "pageview", "bounce_rate", "device", "browser"]):
                boost(["web_analytics"], 1.5)

        # Use very explicit rule for amazon.csv-style ecommerce data
        ecommerce_signals = [
            "product_id",
            "product_name",
            "discounted_price",
            "actual_price",
            "discount_percentage",
            "rating",
            "rating_count",
            "review_id",
            "review_title",
            "review_content",
            "product_link",
            "img_link",
        ]
        if any(col in col_names for col in ecommerce_signals):
            scores["ecommerce"] += 5.0

        # Determine best domain
        best_domain = max(scores, key=lambda d: scores[d])
        best_score = scores[best_domain]

        # Normalize score into a rough confidence 0–1
        # We just compare to a simple scale of 0–10+
        if best_score <= 0:
            return {"type": "unknown", "confidence": 0.0}
        elif best_score < 2:
            confidence = 0.3
        elif best_score < 4:
            confidence = 0.5
        elif best_score < 6:
            confidence = 0.7
        else:
            confidence = 0.9

        return {"type": best_domain, "confidence": confidence}
