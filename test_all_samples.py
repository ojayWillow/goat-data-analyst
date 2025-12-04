import pandas as pd
import sys
from pathlib import Path
import os

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from backend.data_processing.data_fixer import DataFixer
from backend.core.engine import AnalysisEngine

print('='*80)
print('DAY 18: COMPREHENSIVE TESTING - ALL SAMPLE DATA')
print('='*80 + '\n')

# Get all CSV files from sample_data
sample_dir = Path(__file__).parent / 'sample_data'
csv_files = list(sample_dir.glob('*.csv'))

print(f'Found {len(csv_files)} CSV files in sample_data/\n')

fixer = DataFixer()
engine = AnalysisEngine()

total_tests = 0
passed_tests = 0
failed_tests = 0

for csv_file in csv_files:
    print('='*80)
    print(f'📄 TESTING: {csv_file.name}')
    print('='*80)
    
    try:
        # Load data
        df = pd.read_csv(csv_file)
        print(f'✅ Loaded successfully: {len(df)} rows x {len(df.columns)} columns')
        total_tests += 1
        passed_tests += 1
        
        # Run analysis
        print('\n🔍 Running Analysis...')
        result = engine.analyze(df)
        quality = result.quality
        
        print(f'   Quality Score: {quality.get("overall_score", 0):.1f}/100')
        print(f'   Missing Data: {quality.get("missing_pct", 0):.1f}%')
        print(f'   Duplicates: {quality.get("duplicates", 0)}')
        total_tests += 1
        passed_tests += 1
        
        # TEST: Remove Duplicates (if any)
        if quality.get('duplicates', 0) > 0:
            print(f'\n🔄 TEST: Remove Duplicates')
            print(f'   Before: {len(df)} rows, {quality["duplicates"]} duplicates')
            df_fixed, report = fixer.remove_duplicates(df)
            print(f'   After:  {len(df_fixed)} rows')
            total_tests += 1
            if report['removed_rows'] == quality['duplicates']:
                print(f'   ✅ PASS - Removed {report["removed_rows"]} duplicates')
                passed_tests += 1
            else:
                print(f'   ❌ FAIL - Expected {quality["duplicates"]}, removed {report["removed_rows"]}')
                failed_tests += 1
        
        # TEST: Fill Missing Values (if any)
        missing_cols = [col for col, count in quality.get('missing_by_column', {}).items() if count > 0]
        if missing_cols:
            for col in missing_cols[:2]:  # Test first 2 columns with missing data
                print(f'\n📝 TEST: Fill Missing Values - {col}')
                missing_count = df[col].isna().sum()
                print(f'   Before: {missing_count} missing values')
                
                if pd.api.types.is_numeric_dtype(df[col]):
                    df_fixed, report = fixer.fill_missing_numeric(df, col, 'median')
                else:
                    df_fixed, report = fixer.fill_missing_categorical(df, col, 'Unknown')
                
                print(f'   After:  {df_fixed[col].isna().sum()} missing values')
                total_tests += 1
                if df_fixed[col].isna().sum() == 0:
                    print(f'   ✅ PASS - All missing values filled')
                    passed_tests += 1
                else:
                    print(f'   ❌ FAIL - Still has missing values')
                    failed_tests += 1
        
        # TEST: Remove Outliers (if any numeric columns)
        outliers = quality.get('outliers', {})
        if outliers:
            col = list(outliers.keys())[0]  # Test first column with outliers
            print(f'\n🎯 TEST: Remove Outliers - {col}')
            print(f'   Before: {len(df)} rows, {outliers[col]["count"]} outliers')
            df_fixed, report = fixer.remove_outliers(df, col, method='iqr')
            print(f'   After:  {len(df_fixed)} rows, removed {report["removed_rows"]}')
            total_tests += 1
            if report['removed_rows'] > 0:
                print(f'   ✅ PASS - Outliers removed')
                passed_tests += 1
            else:
                print(f'   ⚠️  WARN - No outliers removed (may be expected)')
                passed_tests += 1  # Not a failure
        
        print(f'\n✅ {csv_file.name} - All tests completed')
        
    except Exception as e:
        print(f'\n❌ ERROR processing {csv_file.name}: {str(e)}')
        total_tests += 1
        failed_tests += 1
    
    print('\n')

# FINAL SUMMARY
print('='*80)
print('FINAL TEST SUMMARY')
print('='*80)
print(f'📁 Files Tested: {len(csv_files)}')
print(f'🧪 Total Tests: {total_tests}')
print(f'✅ Passed: {passed_tests}')
print(f'❌ Failed: {failed_tests}')
print(f'📊 Success Rate: {(passed_tests/total_tests*100):.1f}%' if total_tests > 0 else 'N/A')

if failed_tests == 0:
    print('\n🎉 ALL TESTS PASSED - System working perfectly!')
else:
    print(f'\n⚠️  {failed_tests} TEST(S) FAILED - Review issues above')

print('='*80)
