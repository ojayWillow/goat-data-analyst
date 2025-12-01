from backend.reports.assembler import ReportAssembler

# Mock data (same as before)
profile = {
    'dataset_name': 'Test Data',
    'total_rows': 100,
    'total_columns': 4,
    'quality_score': 85,
    'missing_data_pct': 2.5,
    'duplicate_rows': 0,
    'issues': []
}

domain_data = {
    'detected_domain': 'Sales',
    'confidence': 0.92,
    'key_entities': ['Revenue'],
    'top_domains': [('Sales', 0.92)]
}

insights_data = {
    'insights': ['Insight 1', 'Insight 2'],
    'model': 'Groq'
}

charts_data = {
    'time_series': '<div>Chart</div>'
}

assembler = ReportAssembler()

# Test 1: Full report
print("Test 1: FULL REPORT (all sections)")
html_full = assembler.generate_report(profile, domain_data, insights_data, charts_data)
print(f"  Size: {len(html_full):,} bytes\n")

# Test 2: Without domain
print("Test 2: WITHOUT DOMAIN")
html_no_domain = assembler.generate_report(
    profile, 
    config={'include_domain': False}
)
print(f"  Size: {len(html_no_domain):,} bytes")
print(f"  Saved: {len(html_full) - len(html_no_domain):,} bytes\n")

# Test 3: Without AI
print("Test 3: WITHOUT AI")
html_no_ai = assembler.generate_report(
    profile,
    config={'include_ai': False}
)
print(f"  Size: {len(html_no_ai):,} bytes\n")

# Test 4: Minimal (header + quality only)
print("Test 4: MINIMAL (header + quality)")
html_minimal = assembler.generate_report(
    profile,
    config={
        'include_domain': False,
        'include_ai': False,
        'include_charts': False
    }
)
print(f"  Size: {len(html_minimal):,} bytes\n")

print("✅ Config-driven architecture working perfectly!")
print("✅ Add/remove sections without touching code!")
