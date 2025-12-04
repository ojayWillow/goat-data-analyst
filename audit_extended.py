import os

print("\n" + "="*60)
print("🗂️  NON-BACKEND DIRECTORIES")
print("="*60 + "\n")

# Check other directories
other_dirs = {
    'archive/': 'Old code - probably safe to delete',
    'docs/': 'Extra documentation - check if needed',
    'tools/': 'Scripts - check if used',
    '.project/': 'IDE config - safe to delete',
    '.devcontainer/': 'Dev container - keep if using, else delete',
}

for dir_name, description in other_dirs.items():
    if os.path.exists(dir_name):
        # Count files
        file_count = sum([len(files) for _, _, files in os.walk(dir_name)])
        size_kb = sum([os.path.getsize(os.path.join(root, f)) 
                       for root, _, files in os.walk(dir_name) 
                       for f in files]) / 1024
        print(f"📁 {dir_name:20} - {file_count:3} files, {size_kb:6.1f} KB")
        print(f"   → {description}")
    else:
        print(f"⚪ {dir_name:20} - Not found")

print("\n" + "="*60)
print("📋 RECOMMENDED CLEANUP PLAN")
print("="*60 + "\n")

print("✅ DEFINITELY DELETE:")
print("   • backend/api/           - Not imported anywhere")
print("   • backend/connectors/    - Not imported anywhere")
print("   • archive/               - Old code (if exists)")
print("   • .project/              - IDE cruft (if exists)")
print("\n")
print("⚠️  CHECK FIRST (may have value):")
print("   • docs/                  - Extra docs")
print("   • tools/                 - Helper scripts")
print("   • .devcontainer/         - Only if you use it")
print("\n")
print("✅ KEEP:")
print("   • backend/ai/            - Used by engine.py")
print("   • backend/analytics/     - Used by engine.py")  
print("   • backend/core/          - THE BRAIN")
print("   • backend/data_processing/")
print("   • backend/domain_detection/")
print("   • backend/narrative/")
print("   • backend/reports/")
print("   • backend/visualizations/")
print("   • sample_data/           - For testing")
print("   • tests/                 - Tests")
print("   • app.py, main.py        - Entry points")
