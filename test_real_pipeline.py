import pandas as pd
import os
from backend.reports.assembler import ReportAssembler

# 1. Find a CSV file
csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
if not csv_files:
    print("⚠️ No CSV found. Creating dummy data...")
    df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    dataset_name = "Dummy Data"
else:
    print(f"✅ Found CSV: {csv_files[0]}")
    df = pd.read_csv(csv_files[0])
    dataset_name = csv_files[0]

# 2. Mock the analysis results (since we are testing the Assembler, not the analyzers)
profile = {
    'dataset_name': dataset_name,
    'total_rows': len(df),
    'total_columns': len(df.columns),
    'quality_score': 88,
    'missing_data_pct': 0.5,
    'duplicate_rows': 0,
    'issues': []
}

domain_data = {
    'detected_domain': 'Business Operations',
    'confidence': 0.85,
    'key_entities': list(df.columns[:3]),
    'top_domains': [('Operations', 0.85), ('Finance', 0.60)]
}

insights_data = {
    'insights': [
        '1. Data quality is exceptionally high (88/100).',
        '2. Primary domain detected as Business Operations.',
        '3. Key entities identified: ' + ', '.join(df.columns[:3])
    ],
    'model': 'Groq Llama 3'
}

charts_data = {
    'distribution': '<div style="padding:20px; text-align:center; background:#f0f0f0;">📊 Chart Placeholder</div>'
}

# 3. Generate Report via Assembler
print("🚀 Generating report...")
assembler = ReportAssembler()
html = assembler.generate_report(
    profile=profile,
    domain_data=domain_data,
    insights_data=insights_data,
    charts_data=charts_data
)

# 4. Save
output_file = "real_data_report.html"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ Success! Report saved to {output_file} ({len(html):,} bytes)")
