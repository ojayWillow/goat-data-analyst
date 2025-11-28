# Find and read just the domain section method
import re

# Test it first
from backend.domain_detection.domain_detector import DomainDetector
from backend.connectors.csv_handler import CSVHandler

handler = CSVHandler()
df = handler.load_csv('sample_data/train.csv')

detector = DomainDetector()
result = detector.detect_domain(df)

print("[TEST] Domain result:")
print(f"  Primary: {result['primary_domain']}")
print(f"  Confidence: {result['confidence']:.0%}")
print(f"  All scores: {result.get('all_scores', {})}")
print(f"  Row count: {result.get('row_count', 0):,}")

if result.get('all_scores'):
    print("\n[OK] all_scores present!")
    print("Can build chart!")
else:
    print("\n[WARNING] all_scores empty!")
