import ast
import os
from pathlib import Path
from collections import defaultdict

def find_imports(file_path):
    """Extract all imports from a Python file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
        
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
        return imports
    except:
        return []

# Entry points (files that actually RUN)
ENTRY_POINTS = ['app.py', 'main.py', 'backend/core/engine.py', 'backend/core/batch_engine.py']

used_modules = defaultdict(list)

print("🔍 Scanning entry points...\n")

for entry in ENTRY_POINTS:
    if os.path.exists(entry):
        imports = find_imports(entry)
        for imp in imports:
            if imp.startswith('backend.'):
                module = imp.replace('backend.', '').split('.')[0]
                used_modules[module].append(entry)
        print(f"✓ {entry}: {len(imports)} imports")

print("\n" + "="*60)
print("📦 BACKEND MODULES USAGE")
print("="*60 + "\n")

# All backend directories
backend_dirs = [
    'ai', 'analytics', 'api', 'connectors', 'core',
    'data_processing', 'domain_detection', 'narrative',
    'reports', 'visualizations'
]

for module in sorted(backend_dirs):
    if module in used_modules:
        print(f"✅ {module:20} - USED by: {', '.join(set(used_modules[module]))}")
    else:
        print(f"❌ {module:20} - UNUSED")

print("\n" + "="*60)
print("🗑️  SAFE TO DELETE (UNUSED MODULES)")
print("="*60 + "\n")

unused = [m for m in backend_dirs if m not in used_modules]
for module in unused:
    print(f"  backend/{module}/")

print(f"\n💡 Found {len(unused)} unused modules out of {len(backend_dirs)} total")
