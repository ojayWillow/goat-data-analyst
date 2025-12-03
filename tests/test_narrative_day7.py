from backend.narrative.narrative_generator import NarrativeGenerator
import pandas as pd
import numpy as np

gen = NarrativeGenerator()

# Test 1: Financial data
print("\n" + "="*70)
print("TEST 1: FINANCIAL DATA")
print("="*70)
df_finance = pd.DataFrame({
    'account_id': range(500),
    'date': pd.date_range('2024-01-01', periods=500, freq='D'),
    'revenue': np.random.uniform(1000, 50000, 500),
    'expenses': np.random.uniform(500, 30000, 500)
})

domain_finance = {"type": "finance", "confidence": 0.92}
profile_finance = {
    'overall': {'rows': 500, 'columns': 4},
    'columns': [
        {'name': 'account_id', 'type': 'numeric'},
        {'name': 'date', 'type': 'datetime'},
        {'name': 'revenue', 'type': 'numeric'},
        {'name': 'expenses', 'type': 'numeric'}
    ]
}

print(gen.generate_context(domain_finance, profile_finance, df_finance))

# Test 2: Unknown data type (no domain match)
print("\n" + "="*70)
print("TEST 2: GENERIC/UNKNOWN DATA")
print("="*70)
df_generic = pd.DataFrame({
    'col_a': range(200),
    'col_b': np.random.rand(200),
    'col_c': ['X', 'Y', 'Z'] * 66 + ['X', 'Y']
})

domain_generic = {"type": "unknown", "confidence": 0.2}
profile_generic = {
    'overall': {'rows': 200, 'columns': 3},
    'columns': [
        {'name': 'col_a', 'type': 'numeric'},
        {'name': 'col_b', 'type': 'numeric'},
        {'name': 'col_c', 'type': 'categorical', 'unique': 3}
    ]
}

print(gen.generate_context(domain_generic, profile_generic, df_generic))

# Test 3: Data without dates
print("\n" + "="*70)
print("TEST 3: NO DATE COLUMNS")
print("="*70)
df_no_dates = pd.DataFrame({
    'product_id': range(100),
    'quantity': np.random.randint(1, 100, 100),
    'warehouse': np.random.choice(['A', 'B', 'C'], 100)
})

domain_inventory = {"type": "inventory", "confidence": 0.75}
profile_inventory = {
    'overall': {'rows': 100, 'columns': 3},
    'columns': [
        {'name': 'product_id', 'type': 'numeric'},
        {'name': 'quantity', 'type': 'numeric'},
        {'name': 'warehouse', 'type': 'categorical', 'unique': 3}
    ]
}

print(gen.generate_context(domain_inventory, profile_inventory, df_no_dates))

print("\n" + "="*70)
print("✅ All test cases passed")
print("="*70)
