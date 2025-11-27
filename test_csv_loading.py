"""
Quick test script to load and inspect CSV
"""

from backend.connectors.csv_handler import CSVHandler

def test_real_csv():
    print("=" * 60)
    print("Testing CSV Handler with Real Data")
    print("=" * 60)
    
    handler = CSVHandler()
    
    # Load the sample file
    df = handler.load_csv('sample_data/sample_ecommerce.csv')
    
    print("\n✅ CSV Loaded Successfully!")
    print(f"\nShape: {df.shape[0]} rows × {df.shape[1]} columns")
    
    print("\nColumn Names:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i}. {col}")
    
    print("\nFirst 5 rows:")
    print(df.head())
    
    print("\nData Types:")
    print(df.dtypes)
    
    print("\nBasic Statistics:")
    print(df[['quantity', 'price', 'total_amount']].describe())
    
    print("\nMetadata:")
    metadata = handler.get_metadata()
    for key, value in metadata.items():
        if key != 'column_names':  # Skip column names (too long)
            print(f"  {key}: {value}")
    
    print("\n" + "=" * 60)
    print("✅ All tests passed!")
    print("=" * 60)

if __name__ == "__main__":
    test_real_csv()
