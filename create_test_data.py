import pandas as pd
import numpy as np

# Create realistic sales data
np.random.seed(42)
dates = pd.date_range('2023-06-01', periods=500, freq='D')

df = pd.DataFrame({
    'transaction_id': range(1, 501),
    'date': dates,
    'customer_id': np.random.randint(1000, 2000, 500),
    'product': np.random.choice(['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones'], 500),
    'quantity': np.random.randint(1, 5, 500),
    'unit_price': np.random.choice([29.99, 49.99, 799.99, 299.99, 89.99], 500),
    'total_amount': 0.0,
    'region': np.random.choice(['North', 'South', 'East', 'West'], 500),
    'payment_method': np.random.choice(['Credit Card', 'PayPal', 'Bank Transfer'], 500)
})

# Calculate total
df['total_amount'] = df['quantity'] * df['unit_price']

# Add some missing values (realistic)
missing_indices = np.random.choice(df.index, size=15, replace=False)
df.loc[missing_indices, 'customer_id'] = np.nan

# Add a few duplicates
df = pd.concat([df, df.iloc[:5]], ignore_index=True)

df.to_csv('test_sales.csv', index=False)
print(f'✅ Created test_sales.csv: {len(df)} rows')
