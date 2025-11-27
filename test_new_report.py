# test_new_report.py - Simple test for v2.0

from backend.export_engine.quality_report import QualityReportGenerator

# Sample data
sample_profile = {
    'overall': {
        'rows': 50000,
        'columns': 9,
        'memory_mb': 3.43,
        'total_missing': 1250,
        'total_missing_pct': 0.28
    },
    'type_summary': {
        'numeric': 4,
        'categorical': 3,
        'datetime': 1,
        'text': 1
    },
    'columns': [
        {
            'name': 'customer_id',
            'type': 'id',
            'missing_pct': 0.0,
            'unique': 50000,
            'quality_issues': []
        },
        {
            'name': 'age',
            'type': 'numeric',
            'missing_pct': 2.5,
            'unique': 75,
            'quality_issues': ['MANY_OUTLIERS']
        }
    ]
}

sample_quality = {
    'score': 92,
    'status': 'EXCELLENT',
    'issues': [],
    'warnings': ['Column age has 2.5% missing values']
}

print("Testing Quality Report Generator v2.0...")
print("=" * 50)

# Generate report
generator = QualityReportGenerator(sample_profile, sample_quality)
md_path, html_path = generator.save_both('test_v2_report', 'output')

print("\n✅ SUCCESS! Reports generated:")
print(f"   📄 Markdown: {md_path}")
print(f"   🌐 HTML: {html_path}")
print("\nNow open the HTML file in your browser to test the download buttons!")
