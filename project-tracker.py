"""
PROJECT DEPENDENCY TRACKER - Automatic Analysis
For Python Repositories
"""

import ast
import json
import os
from pathlib import Path
from typing import Dict, List, Set, Any, Optional
from dataclasses import dataclass, field, asdict
from collections import defaultdict


def ask_perplexity_about_error(error_type: str, file_name: str) -> str:
    """Get quick explanation from Perplexity about the error."""
    try:
        from openai import OpenAI
        
        client = OpenAI(
            api_key="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",
            base_url="https://api.perplexity.ai",
            timeout=10.0
        )
        
        response = client.chat.completions.create(
            model="sonar",
            messages=[
                {
                    "role": "user",
                    "content": f"Python error '{error_type}' in {file_name}. Explain cause in ONE sentence and fix in ONE sentence. Be super concise."
                }
            ],
            max_tokens=80
        )
        
        return response.choices[0].message.content
    except:
        return ""


@dataclass
class FunctionInfo:
    """Information about a function."""
    name: str
    parameters: List[str] = field(default_factory=list)
    return_annotation: Optional[str] = None
    docstring: Optional[str] = None
    line_number: int = 0


@dataclass
class ClassInfo:
    """Information about a class."""
    name: str
    methods: List[str] = field(default_factory=list)
    bases: List[str] = field(default_factory=list)
    docstring: Optional[str] = None
    line_number: int = 0


@dataclass
class ModuleInfo:
    """Complete information about a Python module."""
    file_path: str
    module_name: str
    imports: List[str] = field(default_factory=list)
    from_imports: Dict[str, List[str]] = field(default_factory=dict)
    functions: List[FunctionInfo] = field(default_factory=list)
    classes: List[ClassInfo] = field(default_factory=list)
    docstring: Optional[str] = None
    size_bytes: int = 0
    line_count: int = 0
    module_type: str = "unknown"


class ProjectAnalyzer:
    """Analyzes Python project structure and dependencies."""
    
    def __init__(self, root_path: Path):
        self.root_path = root_path
        self.modules: Dict[str, ModuleInfo] = {}
        self.dependency_graph: Dict[str, Set[str]] = defaultdict(set)
        
    def find_python_files(self) -> List[Path]:
        """Find all Python files in the project, excluding virtual environments and caches."""
        
        # Directories to exclude
        exclude_dirs = {
            '.venv', 'venv', 'env',  # Virtual environments
            '__pycache__', '.pytest_cache',  # Cache folders
            '.git', '.github',  # Version control
            'node_modules',  # JS dependencies
            '.mypy_cache', '.ruff_cache',  # Linter caches
            'build', 'dist', '.eggs'  # Build artifacts
        }
        
        python_files = []
        for py_file in self.root_path.rglob("*.py"):
            # Check if any excluded directory is in the path
            if not any(excluded in py_file.parts for excluded in exclude_dirs):
                python_files.append(py_file)
        
        return python_files
    
    def get_module_name(self, file_path: Path) -> str:
        """Convert file path to module name."""
        relative = file_path.relative_to(self.root_path)
        parts = list(relative.parts)
        
        # Remove .py extension from last part
        if parts[-1].endswith('.py'):
            parts[-1] = parts[-1][:-3]
        
        # Remove __init__ from module names
        if parts[-1] == '__init__':
            parts = parts[:-1]
        
        return '.'.join(parts) if parts else '__main__'
    
    def classify_module(self, module_info: ModuleInfo) -> str:
        """Classify the type of module based on its contents."""
        has_functions = len(module_info.functions) > 0
        has_classes = len(module_info.classes) > 0
        is_init = module_info.file_path.endswith('__init__.py')
        is_test = 'test' in module_info.module_name.lower()
        is_main = module_info.module_name == '__main__' or 'main' in module_info.file_path
        
        # Determine primary purpose
        if is_init:
            return "package_init"
        elif is_test:
            return "test"
        elif is_main:
            return "main"
        elif 'api' in module_info.module_name.lower() or 'routes' in module_info.module_name.lower():
            return "api"
        elif 'model' in module_info.module_name.lower():
            return "model"
        elif 'utils' in module_info.module_name.lower() or 'helper' in module_info.module_name.lower():
            return "utility"
        elif 'config' in module_info.module_name.lower():
            return "config"
        elif 'connector' in module_info.module_name.lower() or 'handler' in module_info.module_name.lower():
            return "connector"
        elif has_classes and not has_functions:
            return "class_module"
        elif has_functions and not has_classes:
            return "function_module"
        elif has_classes and has_functions:
            return "mixed"
        else:
            return "script"
    
    def analyze_file(self, file_path: Path) -> Optional[ModuleInfo]:
        """Analyze a single Python file."""
        try:
            content = file_path.read_text(encoding='utf-8')
            tree = ast.parse(content, filename=str(file_path))
            
            module_info = ModuleInfo(
                file_path=str(file_path),
                module_name=self.get_module_name(file_path),
                size_bytes=file_path.stat().st_size,
                line_count=len(content.splitlines())
            )
            
            # Extract module docstring
            module_info.docstring = ast.get_docstring(tree)
            
            # Analyze imports and definitions
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        module_info.imports.append(alias.name)
                        self.dependency_graph[module_info.module_name].add(alias.name)
                
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        module_info.from_imports[node.module] = [
                            alias.name for alias in node.names
                        ]
                        self.dependency_graph[module_info.module_name].add(node.module)
                
                elif isinstance(node, ast.FunctionDef):
                    if node.col_offset == 0:  # Top-level function
                        func_info = FunctionInfo(
                            name=node.name,
                            parameters=[arg.arg for arg in node.args.args],
                            return_annotation=ast.unparse(node.returns) if node.returns else None,
                            docstring=ast.get_docstring(node),
                            line_number=node.lineno
                        )
                        module_info.functions.append(func_info)
                
                elif isinstance(node, ast.ClassDef):
                    class_info = ClassInfo(
                        name=node.name,
                        methods=[m.name for m in node.body if isinstance(m, ast.FunctionDef)],
                        bases=[ast.unparse(base) for base in node.bases],
                        docstring=ast.get_docstring(node),
                        line_number=node.lineno
                    )
                    module_info.classes.append(class_info)
            
            # Classify the module
            module_info.module_type = self.classify_module(module_info)
            
            return module_info
            
        except Exception as e:
            error_msg = str(e)
            print(f"⚠️  Error analyzing {file_path}: {error_msg}")
            
            # Get AI explanation from Perplexity
            explanation = ask_perplexity_about_error(error_msg, file_path.name)
            if explanation:
                print(f"   💡 {explanation}")
            
            return None
    
    def analyze_project(self):
        """Analyze entire project."""
        print("\n" + "="*70)
        print("PROJECT DEPENDENCY TRACKER - Automatic Analysis".center(70))
        print("For Python Repositories".center(70))
        print("="*70 + "\n")
        
        print(f"📂 Scanning repository: {self.root_path}")
        python_files = self.find_python_files()
        print(f"✅ Found {len(python_files)} Python files\n")
        
        print("🔍 Analyzing Python files...")
        for i, file_path in enumerate(python_files, 1):
            print(f"  [{i}/{len(python_files)}] {file_path.name}", end='\r')
            module_info = self.analyze_file(file_path)
            if module_info:
                self.modules[module_info.module_name] = module_info
        
        print("\n✅ Analysis complete!\n")
        print("🔗 Building dependency map...")
    
    def generate_summary(self) -> Dict[str, Any]:
        """Generate project summary statistics."""
        total_modules = len(self.modules)
        total_functions = sum(len(m.functions) for m in self.modules.values())
        total_classes = sum(len(m.classes) for m in self.modules.values())
        
        # Count imports
        all_imports = []
        for module in self.modules.values():
            all_imports.extend(module.imports)
            all_imports.extend(module.from_imports.keys())
        
        import_counts = defaultdict(int)
        for imp in all_imports:
            import_counts[imp] += 1
        
        # Module types distribution
        type_distribution = defaultdict(int)
        for module in self.modules.values():
            type_distribution[module.module_type] += 1
        
        # Largest modules
        largest_modules = sorted(
            self.modules.values(),
            key=lambda m: m.size_bytes,
            reverse=True
        )[:5]
        
        return {
            "project_root": str(self.root_path),
            "total_modules": total_modules,
            "total_functions": total_functions,
            "total_classes": total_classes,
            "total_imports": len(all_imports),
            "module_types": dict(type_distribution),
            "top_imports": dict(sorted(import_counts.items(), key=lambda x: x[1], reverse=True)[:5]),
            "largest_modules": [
                {
                    "name": m.module_name,
                    "size_bytes": m.size_bytes,
                    "functions": len(m.functions),
                    "classes": len(m.classes)
                }
                for m in largest_modules
            ]
        }
    
    def print_summary(self, summary: Dict[str, Any]):
        """Print formatted summary to console."""
        print("\n" + "="*70)
        print("📊 PROJECT ANALYSIS SUMMARY")
        print("="*70)
        print(f"📁 Project Root: {summary['project_root']}")
        print(f"📄 Total Modules: {summary['total_modules']}")
        print(f"🔧 Total Functions: {summary['total_functions']}")
        print(f"📦 Total Classes: {summary['total_classes']}")
        print(f"📥 Total Imports: {summary['total_imports']}")
        
        print("\n" + "-"*70)
        print("MODULE TYPES:")
        for mtype, count in summary['module_types'].items():
            print(f"  • {mtype}: {count}")
        
        print("\n" + "-"*70)
        print("TOP 5 MOST IMPORTED MODULES:")
        for module, count in summary['top_imports'].items():
            print(f"  • {module}: imported {count} times")
        
        print("\n" + "-"*70)
        print("TOP 5 LARGEST MODULES:")
        for mod in summary['largest_modules']:
            print(f"  • {mod['name']}: {mod['size_bytes']} bytes, "
                  f"{mod['functions']} functions, {mod['classes']} classes")
        
        print("\n" + "="*70 + "\n")
    
    def save_to_json(self, output_path: Path):
        """Save analysis results to JSON file (optimized)."""
        
        # Lightweight module data - skip docstrings and full AST details
        lightweight_modules = {}
        for name, module in self.modules.items():
            lightweight_modules[name] = {
                "file_path": module.file_path,
                "module_name": module.module_name,
                "module_type": module.module_type,
                "size_bytes": module.size_bytes,
                "line_count": module.line_count,
                "function_count": len(module.functions),
                "class_count": len(module.classes),
                "import_count": len(module.imports) + len(module.from_imports),
                # Only store function/class names, not full details
                "function_names": [f.name for f in module.functions],
                "class_names": [c.name for c in module.classes],
                "imports": module.imports[:10],  # Limit to first 10
                "from_imports": {k: v[:5] for k, v in list(module.from_imports.items())[:10]}  # Limit
            }
        
        data = {
            "modules": lightweight_modules,
            "dependency_graph": {
                k: list(v)[:20] for k, v in self.dependency_graph.items()  # Limit dependencies
            },
            "summary": self.generate_summary()
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Report saved to: {output_path}")


def main():
    # Get current directory
    current_dir = Path.cwd()
    
    # Initialize analyzer
    analyzer = ProjectAnalyzer(current_dir)
    
    # Run analysis
    analyzer.analyze_project()
    
    # Generate and print summary
    summary = analyzer.generate_summary()
    analyzer.print_summary(summary)
    
    # Save to JSON
    output_file = current_dir / "project_structure.json"
    analyzer.save_to_json(output_file)
    
    print(f"\n✨ Analysis complete! Check '{output_file}' for detailed results.")
    print("\n💡 Tip: Use this data to:")
    print("   • Understand module dependencies")
    print("   • Identify circular dependencies")
    print("   • Track function inputs/outputs")
    print("   • Visualize project architecture")
    print("   • Generate documentation automatically")


if __name__ == "__main__":
    main()
