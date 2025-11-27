"""
Test Quality Report v2.0 on Real Datasets
Generates reports for train.csv and customers_50k.csv
"""

from backend.connectors.csv_handler import CSVHandler
from backend.data_processing.profiler import DataProfiler
from backend.export_engine.quality_report import QualityReportGenerator
import time

def test_dataset(file_path, output_name):
    '''Test quality report generation on a dataset'''
    print(f'\n📊 Testing: {file_path}')
    print('=' * 70)
    
    start_time = time.time()
    
    try:
        # Step 1: Load data
        print('Step 1/3: Loading CSV...')
        handler = CSVHandler()
        df = handler.load_csv(file_path)
        print(f'   ✅ Loaded {len(df):,} rows × {len(df.columns)} columns')
        print(f'   📦 Memory: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB')
        
        # Step 2: Profile data
        print('Step 2/3: Profiling data...')
        profiler = DataProfiler()
        profile = profiler.profile_dataframe(df)
        quality = profiler.assess_quality(profile)
        
        print(f'   ✅ Quality Score: {quality[\"score\"]}/100 ({quality[\"status\"]})')
        print(f'   ⚠️  Issues: {len(quality.get(\"issues\", []))}')
        print(f'   ⚠️  Warnings: {len(quality.get(\"warnings\", []))}')
        
        # Step 3: Generate report
        print('Step 3/3: Generating reports...')
        generator = QualityReportGenerator(profile, quality)
        md_path, html_path = generator.save_both(output_name, 'output')
        
        elapsed = time.time() - start_time
        print(f'\n✅ SUCCESS! Completed in {elapsed:.2f} seconds')
        print(f'   📄 Markdown: {md_path}')
        print(f'   🌐 HTML: {html_path}')
        
        return True
        
    except Exception as e:
        print(f'\n❌ ERROR: {str(e)}')
        import traceback
        traceback.print_exc()
        return False

# Main execution
if __name__ == '__main__':
    print('🚀 Quality Report v2.0 - Real Data Testing')
    print('=' * 70)
    
    datasets = [
        ('sample_data/train.csv', 'train_quality_report'),
        ('sample_data/20251127_084222_customers_50k.csv', 'customers_50k_quality_report')
    ]
    
    results = []
    
    for file_path, output_name in datasets:
        success = test_dataset(file_path, output_name)
        results.append((file_path, success))
    
    # Summary
    print('\n' + '=' * 70)
    print('📊 TEST SUMMARY')
    print('=' * 70)
    
    for file_path, success in results:
        status = '✅ PASS' if success else '❌ FAIL'
        print(f'{status} - {file_path}')
    
    total = len(results)
    passed = sum(1 for _, s in results if s)
    
    print(f'\nResults: {passed}/{total} passed')
    
    if passed == total:
        print('\n🎉 ALL TESTS PASSED! Check output/ folder for reports.')
        print('   Open the HTML files in your browser to test download buttons!')
    else:
        print('\n⚠️  Some tests failed. Check errors above.')
