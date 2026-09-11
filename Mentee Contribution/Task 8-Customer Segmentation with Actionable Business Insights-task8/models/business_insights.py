from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

df = pd.read_csv(
    BASE_DIR / "outputs" / "clustered_customers.csv"
)

print("="*60)
print("Business Insights")
print("="*60)

summary = df.groupby("Cluster").agg({
    "Age":"mean",
    "Annual_Income":"mean",
    "Spending_Score":"mean",
    "CustomerID":"count"
})

summary.rename(columns={
    "CustomerID":"Customers"
}, inplace=True)

print(summary)

print("\n" + "="*60)

for cluster in sorted(df["Cluster"].unique()):

    avg_income = summary.loc[cluster, "Annual_Income"]
    avg_spending = summary.loc[cluster, "Spending_Score"]

    print(f"\nCluster {cluster}")

    if avg_income > 70 and avg_spending > 60:
        print("⭐ VIP Customers")
        print("Business Strategy:")
        print("- Premium Membership")
        print("- Early Access Sales")
        print("- Loyalty Rewards")

    elif avg_income > 70 and avg_spending <= 60:
        print("💰 High Income - Low Spending")
        print("Business Strategy:")
        print("- Personalized Discounts")
        print("- Premium Product Recommendations")
        print("- Upselling Campaigns")

    elif avg_income <= 70 and avg_spending > 60:
        print("🛍 Budget Shoppers with High Engagement")
        print("Business Strategy:")
        print("- Bundle Offers")
        print("- Flash Sales")
        print("- Cashback Rewards")

    else:
        print("📦 Average Customers")
        print("Business Strategy:")
        print("- Seasonal Promotions")
        print("- Email Marketing")
        print("- Referral Programs")