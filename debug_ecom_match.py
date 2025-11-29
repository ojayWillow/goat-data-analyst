import pandas as pd
from backend.domain_detection.domain_detector import DomainDetector
from backend.domain_detection.patterns import DomainPatterns

df = pd.read_csv("sample_data/amazon.csv")
detector = DomainDetector()
patterns = detector.patterns

ecom = patterns["e-commerce"]
cols = [c.lower() for c in df.columns]

matches = []
for kw in sorted(ecom.keywords):
    kw_l = kw.lower()
    if any(kw_l in col or col in kw_l for col in cols):
        matches.append(kw)

print("Columns:", cols)
print("Matched e-commerce keywords:", matches)
print("Total keywords:", len(ecom.keywords), "Matched:", len(matches))
