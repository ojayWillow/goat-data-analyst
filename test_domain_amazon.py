import sys
sys.path.insert(0, '.')

import pandas as pd
from backend.domain_detection.detector import DomainDetector

print("\n" + "="*70)
print("DIRECT TEST: DomainDetector on amazon.csv")
print("="*70)

df = pd.read_csv('amazon.csv')
detector = DomainDetector(ai_engine=None)
domain = detector.detect(df)
print('Detected domain:', domain)

print("="*70)
