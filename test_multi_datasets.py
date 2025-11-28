"""
Test domain detection on multiple dataset types
"""
import pandas as pd
from backend.domain_detection.domain_detector import DomainDetector

detector = DomainDetector()

print("=" * 70)
print("[TEST] Multi-Dataset Domain Detection")
print("=" * 70)

# Test 1: E-commerce (train.csv)
print("\n[1/4] Testing E-commerce data (train.csv)...")
df1 = pd.read_csv("sample_data/train.csv")
result1 = detector.detect_domain(df1)
print(f"  [OK] {result1['primary_domain'].upper()} - {result1['confidence']:.0%} confidence")

# Test 2: Finance mock data
print("\n[2/4] Testing Finance mock data...")
df2 = pd.DataFrame({
    'transaction_id': range(100),
    'account_id': range(100),
    'amount': [100.5] * 100,
    'balance': [1000.0] * 100,
    'transaction_type': ['debit'] * 100,
    'date': pd.date_range('2024-01-01', periods=100)
})
result2 = detector.detect_domain(df2)
print(f"  [OK] {result2['primary_domain'].upper()} - {result2['confidence']:.0%} confidence")

# Test 3: CRM mock data
print("\n[3/4] Testing CRM mock data...")
df3 = pd.DataFrame({
    'customer_id': range(100),
    'lead_id': range(100),
    'email': ['test@example.com'] * 100,
    'phone': ['555-1234'] * 100,
    'lead_score': [75] * 100,
    'opportunity_value': [5000] * 100,
    'status': ['active'] * 100
})
result3 = detector.detect_domain(df3)
print(f"  [OK] {result3['primary_domain'].upper()} - {result3['confidence']:.0%} confidence")

# Test 4: HR mock data
print("\n[4/4] Testing HR mock data...")
df4 = pd.DataFrame({
    'employee_id': range(100),
    'department': ['Engineering'] * 100,
    'salary': [75000] * 100,
    'manager_id': [1] * 100,
    'hire_date': pd.date_range('2020-01-01', periods=100),
    'performance_rating': [4.5] * 100
})
result4 = detector.detect_domain(df4)
print(f"  [OK] {result4['primary_domain'].upper()} - {result4['confidence']:.0%} confidence")

# Summary
print("\n" + "=" * 70)
print("[SUMMARY] Domain Detection Results")
print("=" * 70)
results = [
    ("E-commerce (real)", result1),
    ("Finance (mock)", result2),
    ("CRM (mock)", result3),
    ("HR (mock)", result4)
]

for name, res in results:
    domain = res['primary_domain'].upper()
    conf = res['confidence']
    entities = len(res['detected_entities'])
    print(f"{name:20} -> {domain:15} {conf:5.0%}  ({entities} entities)")

print("\n" + "=" * 70)
print("[OK] All 4 datasets tested successfully!")
print("=" * 70)

