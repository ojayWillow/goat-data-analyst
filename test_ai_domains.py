import pandas as pd
from backend.domain_detection.domain_detector import DomainDetector
from backend.domain_detection.ai_domain_detector import AIDomainDetector

files = [
    'sample_data/sample_ecommerce.csv',
    'sample_data/20251127_084222_customers_50k.csv',
    'sample_data/20251126_170320_spotify_data_clean.csv'
]

kw_det = DomainDetector()
ai_det = AIDomainDetector()

for f in files:
    print(f'\n{f}:')
    df = pd.read_csv(f)
    kw = kw_det.detect_domain(df)
    ai = ai_det.enhance_detection(df, kw)
    print(f'Keyword: {kw.get("primary_domain")} {kw.get("confidence"):.1f}%')
    print(f'AI: {ai.get("primary_domain")} {ai.get("confidence"):.1f}%')
    print(f'Reasoning: {ai.get("ai_reasoning", "N/A")[:100]}...')
