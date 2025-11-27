"""
Test ALL CSV files in sample_data folder
"""

from backend.connectors.csv_handler import CSVHandler
import os
from pathlib import Path

def test_all_csvs():
    print("=" * 80)
    print("🧪 TESTING ALL CSV FILES")
    print("=" * 80)
    
    # Get all CSV files in sample_data folder
    sample_dir = Path('sample_data')
    csv_files = list(sample_dir.glob('*.csv'))
    
    print(f"\n📊 Found {len(csv_files)} CSV files to test\n")
    
    results = []
    
    for i, csv_file in enumerate(csv_files, 1):
        print(f"\n{'='*80}")
        print(f"TEST {i}/{len(csv_files)}: {csv_file.name}")
        print('='*80)
        
        handler = CSVHandler()
        
        try:
            # Try to load the CSV
            df = handler.load_csv(str(csv_file))
            metadata = handler.get_metadata()
            
            print(f"✅ SUCCESS!")
            print(f"\n📏 Shape: {df.shape[0]} rows × {df.shape[1]} columns")
            print(f"📝 Encoding: {metadata['encoding']}")
            print(f"🔸 Delimiter: '{metadata['delimiter']}'")
            
            print(f"\n📋 Column Names ({len(df.columns)}):")
            for j, col in enumerate(df.columns, 1):
                dtype = df[col].dtype
                print(f"  {j}. {col} ({dtype})")
            
            print(f"\n🔍 First 3 rows:")
            print(df.head(3).to_string())
            
            # Check for missing values
            missing = df.isnull().sum()
            if missing.sum() > 0:
                print(f"\n⚠️  Missing Values Found:")
                for col, count in missing[missing > 0].items():
                    pct = (count / len(df)) * 100
                    print(f"  - {col}: {count} ({pct:.1f}%)")
            else:
                print(f"\n✅ No missing values!")
            
            # Numeric columns statistics
            numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
            if len(numeric_cols) > 0:
                print(f"\n📊 Numeric Columns Statistics:")
                print(df[numeric_cols].describe().to_string())
            
            results.append({
                'file': csv_file.name,
                'status': 'SUCCESS',
                'rows': df.shape[0],
                'columns': df.shape[1],
                'encoding': metadata['encoding'],
                'delimiter': metadata['delimiter']
            })
            
        except Exception as e:
            print(f"❌ FAILED!")
            print(f"Error: {str(e)}")
            
            results.append({
                'file': csv_file.name,
                'status': 'FAILED',
                'error': str(e)
            })
    
    # Summary
    print(f"\n{'='*80}")
    print("📊 SUMMARY")
    print('='*80)
    
    success_count = sum(1 for r in results if r['status'] == 'SUCCESS')
    fail_count = len(results) - success_count
    
    print(f"\n✅ Successful: {success_count}/{len(results)}")
    print(f"❌ Failed: {fail_count}/{len(results)}")
    
    if success_count > 0:
        print(f"\n✅ SUCCESSFUL FILES:")
        for r in results:
            if r['status'] == 'SUCCESS':
                print(f"  - {r['file']}: {r['rows']} rows, {r['columns']} cols, {r['encoding']}, '{r['delimiter']}'")
    
    if fail_count > 0:
        print(f"\n❌ FAILED FILES:")
        for r in results:
            if r['status'] == 'FAILED':
                print(f"  - {r['file']}: {r['error']}")
    
    print(f"\n{'='*80}")
    
    if fail_count == 0:
        print("🎉 ALL FILES LOADED SUCCESSFULLY!")
    else:
        print(f"⚠️  {fail_count} files need attention")
    
    print('='*80)

if __name__ == "__main__":
    test_all_csvs()
