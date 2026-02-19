# Data Analysis Key Findings

## Missing Values Handling
- Missing values in the 'Postal Code' column were successfully handled by dropping the corresponding rows, resulting in zero missing values for this column.

## Data Type Conversion
- The 'Order Date' and 'Ship Date' columns were successfully converted to datetime objects using the format '%d/%m/%Y', after an initial attempt failed due to incorrect format inference.

## Column Name Standardization
- All column names were converted to snake_case (e.g., 'Order Date' became 'order_date') for consistency.

## Irrelevant Column Removal
- Seven columns identified as irrelevant were dropped from the dataset:
  - row_id
  - order_id
  - customer_id
  - product_id
  - customer_name
  - product_name
  - country

## Sales Statistics
- The 'Sales' column was converted to a NumPy array, and its key statistics were calculated:
  - **Mean Sales:** $230.12
  - **Median Sales:** $54.38
  - **Standard Deviation of Sales:** $625.27

## Feature and Target Separation
- The dataset was successfully split into:
  - **Features (X):** All columns except 'sales'
  - **Target Variable (y):** The 'sales' column

---

# Insights or Next Steps

The dataset is now cleaned and prepared, with appropriate data types, standardized column names, and handled missing values, making it ready for:

- Exploratory data analysis
- Feature engineering
- Predictive modeling

Further analysis could involve:
- Exploring relationships between the remaining features and the 'sales' target variable
- Developing a predictive model using the separated X and y datasets