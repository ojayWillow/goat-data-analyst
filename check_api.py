from backend.export_engine.quality_report import QualityReportGenerator
import inspect

# Get the signature
sig = inspect.signature(QualityReportGenerator.generate_html)
print(f"[API] generate_html signature: {sig}")

# Get the source
print("\n[SOURCE] generate_html method:")
source_lines = inspect.getsource(QualityReportGenerator.generate_html).split('\n')[:10]
for line in source_lines:
    print(line)

# Also check __init__
init_sig = inspect.signature(QualityReportGenerator.__init__)
print(f"\n[INIT] __init__ signature: {init_sig}")

# Check for to_html method
if hasattr(QualityReportGenerator, 'to_html'):
    print("[OK] Has to_html method")

# List all methods
print("\n[METHODS]:")
methods = [m for m in dir(QualityReportGenerator) if not m.startswith('_') and callable(getattr(QualityReportGenerator, m))]
for method in methods:
    print(f"  - {method}")
