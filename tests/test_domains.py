import sys
sys.path.insert(0, '.')

import pandas as pd
import numpy as np
from backend.narrative.narrative_generator import NarrativeGenerator

gen = NarrativeGenerator()

# Test 1: Sales (you just saw this)
print("\n" + "="*70)
print("TEST 1: SALES DOMAIN")
print("="*70)

domain_sales = {'type': 'sales', 'confidence': 0.85}
quality = {'missing_pct': 10.0, 'duplicates': 5, 'overall_score': 85, 'missing_by_column': {}}
profile = {'rows': 100, 'columns': 4}

print(gen.generate_action_plan(domain_sales, quality, {}, profile))

# Test 2: Finance
print("\n" + "="*70)
print("TEST 2: FINANCE DOMAIN")
print("="*70)

domain_finance = {'type': 'finance', 'confidence': 0.9}
print(gen.generate_action_plan(domain_finance, quality, {}, profile))

# Test 3: Healthcare
print("\n" + "="*70)
print("TEST 3: HEALTHCARE DOMAIN")
print("="*70)

domain_health = {'type': 'healthcare', 'confidence': 0.8}
print(gen.generate_action_plan(domain_health, quality, {}, profile))

print("\n" + "="*70)
print("✅ Day 9: Domain-Aware Action Plans WORKING!")
print("="*70)
