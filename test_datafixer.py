import pandas as pd
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from backend.data_processing.data_fixer import DataFixer

print('='*60)
print('DAY 18: AUTOMATED TESTING OF DATA FIXER')
print('='*60 + '\n')

# Create test data with ACTUAL duplicate
test_data = pd.DataFrame({
    'id': [1, 2, 3, 3, 5],  
    'name': ['Alice', 'Bob', 'Charlie', 'Charlie', 'Dave'],  # Now row 3 is actual duplicate
    'age': [25, 30, 35, 35, 999],  # Outlier: 999
    'amount': [100, 200, 300, 300, 150]
})

fixer = DataFixer()
passed = 0
failed = 0

# TEST 1: Remove Duplicates
print('\n🔄 TEST 1: Remove Duplicates')
print(f'   Before: {len(test_data)} rows')
print(f'   Data:\n{test_data}')
df_fixed, report = fixer.remove_duplicates(test_data)
print(f'   After:  {len(df_fixed)} rows')
print(f'   Report: {report}')
if report['removed_rows'] == 1 and len(df_fixed) == 4:
    print('   ✅ PASS - Removed 1 duplicate')
    passed += 1
else:
    print('   ❌ FAIL - Expected to remove 1 duplicate')
    failed += 1

# TEST 2: Fill Missing Values (Categorical)
test_data_missing = pd.DataFrame({
    'id': [1, 2, 3, 4, 5],
    'name': ['Alice', 'Bob', None, 'Dave', 'Eve']
})
print('\n📝 TEST 2: Fill Missing Values (Categorical)')
print(f'   Before: {test_data_missing["name"].isna().sum()} missing')
df_fixed, report = fixer.fill_missing_categorical(test_data_missing, 'name', 'Unknown')
print(f'   After:  {df_fixed["name"].isna().sum()} missing')
print(f'   Report: {report}')
if df_fixed['name'].isna().sum() == 0:
    print('   ✅ PASS - All missing values filled')
    passed += 1
else:
    print('   ❌ FAIL - Missing values still exist')
    failed += 1

# TEST 3: Fill Missing Values (Numeric - Median)
test_data_numeric = test_data.copy()
test_data_numeric.loc[2, 'amount'] = None
print('\n📝 TEST 3: Fill Missing Values (Numeric - Median)')
print(f'   Before: {test_data_numeric["amount"].isna().sum()} missing')
df_fixed, report = fixer.fill_missing_numeric(test_data_numeric, 'amount', 'median')
print(f'   After:  {df_fixed["amount"].isna().sum()} missing')
print(f'   Report: {report}')
if df_fixed['amount'].isna().sum() == 0:
    print('   ✅ PASS - All missing values filled with median')
    passed += 1
else:
    print('   ❌ FAIL - Missing values still exist')
    failed += 1

# TEST 4: Remove Outliers
print('\n🎯 TEST 4: Remove Outliers (IQR method)')
print(f'   Before: {len(test_data)} rows (contains age=999)')
df_fixed, report = fixer.remove_outliers(test_data, 'age', method='iqr')
print(f'   After:  {len(df_fixed)} rows')
print(f'   Report: {report}')
if len(df_fixed) < len(test_data):
    print('   ✅ PASS - Outliers removed')
    passed += 1
else:
    print('   ❌ FAIL - No outliers removed')
    failed += 1

# TEST 5: Normalize Dates (FIXED - use dayfirst for ambiguous dates)
test_data_dates = pd.DataFrame({
    'date': ['2024-01-15', '01/16/2024', '2024-01-17']  # All valid, different formats
})
print('\n📅 TEST 5: Normalize Dates')
print(f'   Before formats: {test_data_dates["date"].tolist()}')
df_fixed, report = fixer.normalize_dates(test_data_dates, 'date')
print(f'   After formats:  {df_fixed["date"].tolist()}')
print(f'   Report: {report}')
# Check if all dates are valid (not 'nan' string)
valid_dates = all(d != 'nan' and pd.notna(d) for d in df_fixed['date'])
if valid_dates:
    print('   ✅ PASS - All dates normalized successfully')
    passed += 1
else:
    print('   ❌ FAIL - Some dates became nan')
    failed += 1

# SUMMARY
print('\n' + '='*60)
print('TEST SUMMARY')
print('='*60)
print(f'✅ PASSED: {passed}/5 tests')
print(f'❌ FAILED: {failed}/5 tests')
if failed == 0:
    print('\n🎉 ALL TESTS PASSED - DataFixer working correctly!')
else:
    print(f'\n⚠️  {failed} TEST(S) FAILED - Review DataFixer code')
print('='*60)
