import pandas as pd
from backend.reports.assembler import ReportAssembler

# Create sample data
df = pd.DataFrame({
    'Date': pd.date_range('2024-01-01', periods=100),
    'Revenue': [1000 + i*10 for i in range(100)],
    'Customers': [50 + i for i in range(100)],
    'Region': ['US', 'EU', 'ASIA'] * 33 + ['US']
})

# Mock profile data
profile = {
    'dataset_name': 'Sales Data Q4 2024',
    'total_rows': 100,
    'total_columns': 4,
    'quality_score': 85,
    'missing_data_pct': 2.5,
    'duplicate_rows': 0,
    'issues': ['Minor: 2.5% missing in Revenue column']
}

# Mock domain data
domain_data = {
    'detected_domain': 'Sales & Revenue',
    'confidence': 0.92,
    'key_entities': ['Revenue', 'Customers', 'Region', 'Sales'],
    'top_domains': [('Sales', 0.92), ('E-commerce', 0.78), ('Finance', 0.65)]
}

# Mock AI insights
insights_data = {
    'insights': [
        '1. Revenue shows consistent upward trend (+1000/day)',
        '2. Customer acquisition stable at ~1 new customer/day',
        '3. ASIA region has highest transaction volume',
        '4. No anomalies detected in time series'
    ],
    'model': 'Groq Llama'
}

# Mock charts
charts_data = {
    'time_series': '<div>📈 Time Series Chart Would Go Here</div>',
    'distribution': '<div>📊 Distribution Chart Would Go Here</div>'
}

# Generate report with assembler
assembler = ReportAssembler()
html = assembler.generate_report(
    profile=profile,
    domain_data=domain_data,
    insights_data=insights_data,
    charts_data=charts_data,
    config={
        'include_header': True,
        'include_quality': True,
        'include_domain': True,
        'include_ai': True,
        'include_charts': True,
        'include_footer': True
    }
)

# Save to file
# Save to file with UTF-8 encoding
with open('test_report.html', 'w', encoding='utf-8') as f:
    f.write(html)


print('✅ Report generated successfully!')
print(f'✅ HTML size: {len(html):,} bytes')
print('✅ Saved to: test_report.html')
