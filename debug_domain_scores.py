import pandas as pd
from backend.domain_detection.domain_detector import DomainDetector

df = pd.read_csv("sample_data/amazon.csv")
detector = DomainDetector()

result = detector.detect_domain(df)
print(result)
