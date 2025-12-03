# ============================================================================
# Batch Engine - Multi-File Analysis
# ============================================================================
# Day 14: Analyze multiple CSV files at once
# 
# Capabilities:
# - Scan folder for all CSVs
# - Run AnalysisEngine on each file
# - Aggregate results into company-level summary
# - Prioritize files by data quality issues
# ============================================================================

import os
import sys
from pathlib import Path
from typing import List, Dict, Optional
import pandas as pd

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.core.engine import AnalysisEngine
from backend.core.models import AnalysisResult


class BatchEngine:
    """
    Analyze multiple CSV files and generate company-level insights
    
    Use this to scan entire folders or analyze multiple files,
    then get aggregated health scores and prioritized action plans.
    """
    
    def __init__(self):
        """Initialize the batch analyzer"""
        self.engine = AnalysisEngine()
        print("✓ BatchEngine initialized")
    
    def analyze_folder(self, folder_path: str) -> Dict:
        """
        Analyze all CSV files in a folder
        
        Args:
            folder_path: Path to folder containing CSV files
        
        Returns:
            {
                'files': [AnalysisResult, ...],
                'summary': {
                    'total_files': int,
                    'total_rows': int,
                    'avg_quality_score': float,
                    'total_issues': int,
                    'files_needing_attention': [filename, ...],
                    'top_issues': [issue, ...]
                }
            }
        """
        folder = Path(folder_path)
        
        if not folder.exists():
            raise FileNotFoundError(f"Folder not found: {folder_path}")
        
        # Find all CSV files
        csv_files = list(folder.glob("*.csv"))
        
        if not csv_files:
            raise ValueError(f"No CSV files found in {folder_path}")
        
        print(f"\n{'='*70}")
        print(f"BATCH ANALYSIS: {len(csv_files)} files found")
        print(f"{'='*70}")
        
        # Analyze each file
        results = []
        for csv_file in csv_files:
            print(f"\n📄 Analyzing: {csv_file.name}")
            try:
                df = pd.read_csv(csv_file)
                result = self.engine.analyze(df)
                result.filename = csv_file.name  # Store filename
                results.append(result)
                print(f"   ✅ Complete - Quality: {result.quality.get('overall_score', 0):.0f}/100")
            except Exception as e:
                print(f"   ❌ Error: {e}")
                # Create error result
                error_result = AnalysisResult(dataframe=pd.DataFrame())
                error_result.filename = csv_file.name
                error_result.errors = [str(e)]
                results.append(error_result)
        
        # Generate summary
        summary = self._generate_summary(results)
        
        print(f"\n{'='*70}")
        print(f"SUMMARY: {summary['total_files']} files analyzed")
        print(f"Average Quality: {summary['avg_quality_score']:.1f}/100")
        print(f"Files Needing Attention: {len(summary['files_needing_attention'])}")
        print(f"{'='*70}\n")
        
        return {
            'files': results,
            'summary': summary
        }
    
    def analyze_files(self, file_paths: List[str]) -> Dict:
        """
        Analyze specific list of CSV files
        
        Args:
            file_paths: List of paths to CSV files
        
        Returns:
            Same format as analyze_folder()
        """
        print(f"\n{'='*70}")
        print(f"BATCH ANALYSIS: {len(file_paths)} files")
        print(f"{'='*70}")
        
        results = []
        for file_path in file_paths:
            file_path = Path(file_path)
            print(f"\n📄 Analyzing: {file_path.name}")
            try:
                df = pd.read_csv(file_path)
                result = self.engine.analyze(df)
                result.filename = file_path.name
                results.append(result)
                print(f"   ✅ Complete - Quality: {result.quality.get('overall_score', 0):.0f}/100")
            except Exception as e:
                print(f"   ❌ Error: {e}")
                error_result = AnalysisResult(dataframe=pd.DataFrame())
                error_result.filename = file_path.name
                error_result.errors = [str(e)]
                results.append(error_result)
        
        summary = self._generate_summary(results)
        
        print(f"\n{'='*70}")
        print(f"SUMMARY: {summary['total_files']} files analyzed")
        print(f"Average Quality: {summary['avg_quality_score']:.1f}/100")
        print(f"{'='*70}\n")
        
        return {
            'files': results,
            'summary': summary
        }
    
    def _generate_summary(self, results: List[AnalysisResult]) -> Dict:
        """
        Generate company-level summary from multiple file results
        
        Args:
            results: List of AnalysisResult objects
        
        Returns:
            Summary dictionary with aggregated metrics
        """
        total_files = len(results)
        total_rows = sum(r.profile.get('rows', r.profile.get('overall', {}).get('rows', 0)) for r in results)
        
        # Calculate average quality score
        quality_scores = [r.quality.get('overall_score', 0) for r in results if not r.errors]
        avg_quality_score = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        
        # Find files needing attention (quality < 70)
        files_needing_attention = [
            {
                'filename': r.filename,
                'quality_score': r.quality.get('overall_score', 0),
                'issues': self._summarize_issues(r.quality)
            }
            for r in results 
            if r.quality.get('overall_score', 0) < 70 and not r.errors
        ]
        
        # Sort by quality score (worst first)
        files_needing_attention.sort(key=lambda x: x['quality_score'])
        
        # Aggregate top issues across all files
        all_issues = []
        for r in results:
            if r.errors:
                continue
            quality = r.quality
            
            # Missing data
            missing_pct = quality.get('missing_pct', 0)
            if missing_pct > 5:
                all_issues.append({
                    'type': 'missing_data',
                    'severity': 'high' if missing_pct > 20 else 'medium',
                    'count': 1,
                    'description': f"Missing data ({missing_pct:.1f}%)"
                })
            
            # Duplicates
            duplicates = quality.get('duplicates', 0)
            if duplicates > 0:
                all_issues.append({
                    'type': 'duplicates',
                    'severity': 'high' if duplicates > 100 else 'medium',
                    'count': duplicates,
                    'description': f"Duplicate rows ({duplicates})"
                })
            
            # Outliers
            outliers = quality.get('outliers', {})
            if outliers:
                all_issues.append({
                    'type': 'outliers',
                    'severity': 'medium',
                    'count': len(outliers),
                    'description': f"Outliers in {len(outliers)} columns"
                })
            
            # Date format issues
            date_issues = quality.get('date_format_issues', {})
            if date_issues:
                all_issues.append({
                    'type': 'date_formats',
                    'severity': 'medium',
                    'count': len(date_issues),
                    'description': f"Date format issues in {len(date_issues)} columns"
                })
            
            # Capitalization issues
            cap_issues = quality.get('capitalization_issues', {})
            if cap_issues:
                all_issues.append({
                    'type': 'capitalization',
                    'severity': 'low',
                    'count': len(cap_issues),
                    'description': f"Capitalization issues in {len(cap_issues)} columns"
                })
        
        # Count issues by type
        issue_counts = {}
        for issue in all_issues:
            issue_type = issue['type']
            if issue_type not in issue_counts:
                issue_counts[issue_type] = {
                    'type': issue_type,
                    'count': 0,
                    'severity': issue['severity'],
                    'description': issue['description'].split('(')[0].strip()
                }
            issue_counts[issue_type]['count'] += 1
        
        # Sort by severity and count
        severity_order = {'high': 0, 'medium': 1, 'low': 2}
        top_issues = sorted(
            issue_counts.values(),
            key=lambda x: (severity_order[x['severity']], -x['count'])
        )[:5]
        
        return {
            'total_files': total_files,
            'total_rows': total_rows,
            'avg_quality_score': avg_quality_score,
            'total_issues': len(all_issues),
            'files_needing_attention': files_needing_attention,
            'top_issues': top_issues
        }
    
    def _summarize_issues(self, quality: Dict) -> List[str]:
        """Summarize quality issues for a single file"""
        issues = []
        
        missing_pct = quality.get('missing_pct', 0)
        if missing_pct > 5:
            issues.append(f"Missing data: {missing_pct:.1f}%")
        
        duplicates = quality.get('duplicates', 0)
        if duplicates > 0:
            issues.append(f"Duplicates: {duplicates}")
        
        outliers = quality.get('outliers', {})
        if outliers:
            issues.append(f"Outliers in {len(outliers)} columns")
        
        date_issues = quality.get('date_format_issues', {})
        if date_issues:
            issues.append(f"Date format issues")
        
        cap_issues = quality.get('capitalization_issues', {})
        if cap_issues:
            issues.append(f"Capitalization issues")
        
        return issues if issues else ["No major issues"]


# Test function
def _test():
    """Test batch engine with sample data"""
    import tempfile
    import shutil
    
    print("\n" + "="*70)
    print("TESTING BATCH ENGINE")
    print("="*70)
    
    # Create temp folder with sample CSVs
    temp_dir = tempfile.mkdtemp()
    print(f"\nCreated temp folder: {temp_dir}")
    
    try:
        # Create 3 sample CSVs with different quality levels
        
        # File 1: Clean data
        df1 = pd.DataFrame({
            'id': range(100),
            'amount': range(100, 200),
            'category': ['A'] * 50 + ['B'] * 50
        })
        df1.to_csv(os.path.join(temp_dir, 'clean_data.csv'), index=False)
        
        # File 2: Messy data (missing values, duplicates)
        df2 = pd.DataFrame({
            'id': list(range(50)) + list(range(50)),  # Duplicates
            'amount': [None] * 20 + list(range(80)),  # Missing
            'category': ['A'] * 100
        })
        df2.to_csv(os.path.join(temp_dir, 'messy_data.csv'), index=False)
        
        # File 3: Medium quality
        df3 = pd.DataFrame({
            'id': range(200),
            'amount': [None] * 10 + list(range(190)),  # Some missing
            'category': ['A'] * 100 + ['B'] * 100
        })
        df3.to_csv(os.path.join(temp_dir, 'medium_data.csv'), index=False)
        
        print("Created 3 sample CSV files")
        
        # Run batch analysis
        batch = BatchEngine()
        result = batch.analyze_folder(temp_dir)
        
        print("\n✅ Batch analysis complete!")
        print(f"   Files analyzed: {result['summary']['total_files']}")
        print(f"   Total rows: {result['summary']['total_rows']:,}")
        print(f"   Avg quality: {result['summary']['avg_quality_score']:.1f}/100")
        print(f"   Files needing attention: {len(result['summary']['files_needing_attention'])}")
        
        if result['summary']['top_issues']:
            print("\n   Top issues across all files:")
            for issue in result['summary']['top_issues']:
                print(f"      - {issue['description']}: {issue['count']} files")
        
    finally:
        # Cleanup
        shutil.rmtree(temp_dir)
        print(f"\n🧹 Cleaned up temp folder")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    _test()
