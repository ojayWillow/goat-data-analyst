from backend.connectors.csv_handler import CSVHandler
from backend.domain_detection.domain_detector import DomainDetector

print("🔄 Loading train.csv...")
handler = CSVHandler()
df = handler.load_csv('sample_data/train.csv')
print(f"✅ Loaded {len(df):,} rows × {len(df.columns)} columns\n")

print("🔍 Detecting domain...")
detector = DomainDetector()
result = detector.detect_domain(df)

print("\n" + "="*60)
print("📊 DOMAIN DETECTION RESULTS")
print("="*60)

# Show summary
summary = detector.get_domain_summary(result)
print(summary)

# Show all domain scores
print("\n📈 All Domain Scores:")
for domain, score in sorted(result['all_scores'].items(), key=lambda x: x[1], reverse=True):
    bar = "█" * int(score * 50)
    print(f"  {domain:12} {score:.3f} {bar}")

# Show recommendations
print(f"\n💡 Recommendations ({len(result['recommendations'])}):")
for i, rec in enumerate(result['recommendations'][:7], 1):
    print(f"  {i}. {rec}")

if len(result['recommendations']) > 7:
    print(f"  ... and {len(result['recommendations']) - 7} more")

print("\n" + "="*60)
print("✅ Domain detection complete!")
print("="*60)
