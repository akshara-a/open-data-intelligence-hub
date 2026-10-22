import pandas as pd
import numpy as np

np.random.seed(42)

n_rows = 1500

categories = ["Electronics", "Furniture", "Clothing", "Groceries", "Sports"]
regions = ["North", "South", "East", "West"]
customer_types = ["New", "Returning", "Premium"]
payment_methods = ["UPI", "Credit Card", "Debit Card", "Cash"]

data = {
    "Order_ID": range(10001, 10001 + n_rows),
    "Order_Date": pd.date_range(
        start="2024-01-01",
        periods=n_rows,
        freq="D"
    ),
    "Category": np.random.choice(categories, n_rows),
    "Region": np.random.choice(regions, n_rows),
    "Customer_Type": np.random.choice(customer_types, n_rows),
    "Payment_Method": np.random.choice(payment_methods, n_rows),
    "Quantity": np.random.randint(1, 10, n_rows),
    "Unit_Price": np.round(
        np.random.uniform(100, 5000, n_rows),
        2
    ),
    "Discount": np.round(
        np.random.uniform(0, 0.30, n_rows),
        2
    ),
    "Profit": np.round(
        np.random.uniform(50, 3000, n_rows),
        2
    )
}

df = pd.DataFrame(data)

# Create Sales column
df["Sales"] = np.round(
    df["Quantity"] * df["Unit_Price"] * (1 - df["Discount"]),
    2
)

# Introduce some missing values
df.loc[
    np.random.choice(df.index, 40, replace=False),
    "Customer_Type"
] = np.nan

df.loc[
    np.random.choice(df.index, 30, replace=False),
    "Profit"
] = np.nan

# Introduce inconsistent text formatting
df.loc[df.sample(25, random_state=1).index, "Category"] = " electronics "
df.loc[df.sample(20, random_state=2).index, "Region"] = "north "

# Add duplicate rows
duplicates = df.sample(25, random_state=42)

df = pd.concat([df, duplicates], ignore_index=True)

output_path = (
    "Mentee Contribution/Task 4 - Data Analysis using Pandas/"
    "SNITHINKUMAR/data/retail_sales_dataset.csv"
)

df.to_csv(output_path, index=False)

print("Dataset created successfully!")
print("Dataset shape:", df.shape)
print("Saved to:", output_path)