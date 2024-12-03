import numpy as np
import pandas as pd

num_restraunts = 100
num_samples = 100_000

# Define the price ranges for each food category
Category_Prices = {
    "Meat": (15, 50),      # Price range for meat dishes
    "Fish": (12, 50),     # Price range for fish dishes
    "Pasta": (10, 25),   # Price range for pasta dishes
    "Salad": (10, 20),     # Price range for salad dishes
    "Dessert": (5, 10)    # Price range for desserts
}

# Define other parameters for categories
Categories = {
    0 : {"avg_sales_mean": 90, "avg_sales_std": 15, "avg_consumption_rate": (0.65, 1.0)}, # NO CHANGES
    1 : {"avg_sales_mean": 60, "avg_sales_std": 10, "avg_consumption_rate": (0.4, 0.64)}, # REDUCE PLATE SIZE
    2 : {"avg_sales_mean": 25, "avg_sales_std": 5,  "avg_consumption_rate": (0.2, 0.4)},  # REDUCE PLATE SIZE AND STOCK
    3 : {"avg_sales_mean": 5, "avg_sales_std": 2,   "avg_consumption_rate": (0.0, 0.2)},  # REMOVE FROM MENU
}

data = []

for label, ranges in Categories.items():
    # Generate monthly sales based on normal distribution
    sales = np.random.normal(ranges["avg_sales_mean"], ranges["avg_sales_std"], num_samples).astype(int)
    sales = np.clip(sales, 0, 100)
    
    consumption_rate = np.random.uniform(*ranges["avg_consumption_rate"], num_samples)
    
    for _ in range(num_samples // 4):
        # Randomly choose one of the 5 categories for each sample (Meat, Fish, Pasta, Salad, Dessert)
        chosen_category = np.random.choice(list(Category_Prices.keys()))
        
        # Get price range for the chosen category
        price_range = Category_Prices[chosen_category]
        
        # Generate price and calculate AVC
        price = np.random.uniform(*price_range)
        avc = np.random.uniform(0.3, 0.6)
        avc_value = price * avc
        
        # Append data for the current sample
        data.append({
            "Sales": sales[_],
            "Stock Remaining (%)" : round(1 - (sales[_] / 100), 2),
            "Avg_consumption Rate (%)": round(consumption_rate[_], 2),
            "Price": round(price, 2),
            "AVC": round(avc_value, 2),
            "Category": chosen_category,
            "Label": label
        })

# Convert to DataFrame
df = pd.DataFrame(data)

# Save the dataset
df.to_csv("food_wastage_classification_dataset_total.csv", index=False)

# Show first few rows of the dataset
print(df.head())