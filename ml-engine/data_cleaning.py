# Branch name - day-4-data-cleaning

import pandas as pd
import numpy as np


file_path = "data/raw/train.csv"
df = pd.read_csv(file_path)

print("Original Shape:", df.shape)

print(df.columns)

print("\nMissing Values Before Cleaning:\n")
print(df.isnull().sum())

# =====================================
# Handle Missing Values
# =====================================

df.dropna(subset=['Postal Code'], inplace=True)
print(df['Postal Code'].isnull().sum())

# =====================================
# Remove Unnecessary Columns
# (Row ID not useful for ML)
# =====================================

df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%d/%m/%Y')
print(df.info())

df.columns = df.columns.str.lower().str.replace(' ', '_')

columns_to_drop = ['row_id', 'order_id', 'customer_id', 'product_id', 'customer_name', 'product_name', 'country']
df = df.drop(columns=columns_to_drop)
print(df.columns)


# =====================================
# Feature and Target Separation
# =====================================

# Sales is our target variable
X = df.drop(columns=['sales'])
y = df['sales']

print("Features (X) head:")
print(X.head())
print("\nTarget (y) head:")
print(y.head())

# =====================================
# NumPy Operations on Sales
# =====================================

sales_array = df['sales'].to_numpy()

mean_sales = np.mean(sales_array)
median_sales = np.median(sales_array)
std_sales = np.std(sales_array)

print(f"Mean Sales: {mean_sales:.2f}")
print(f"Median Sales: {median_sales:.2f}")
print(f"Standard Deviation of Sales: {std_sales:.2f}")

# =====================================
# Save Cleaned Dataset
# =====================================

output_path = "data/processed/cleaned_superstore.csv"
df.to_csv(output_path, index=False)

print("\nCleaned dataset saved to data/processed/")
print("Final Shape:", df.shape)


# =====================================
# Explanation
# =====================================

# Why NumPy is faster than Python lists?
# - Uses contiguous memory storage.
# - Vectorized operations (no Python loops).
# - Implemented in C.
# - Optimized for numerical computation.
