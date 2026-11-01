# ==========================================
# Customer Segment Profiling
# ==========================================

import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------------------
# Load Clustered Dataset
# ------------------------------------------

df = pd.read_csv("reports/customer_segments.csv")

print("=" * 60)
print("CUSTOMER SEGMENT PROFILING")
print("=" * 60)

print("\nDataset Shape:")
print(df.shape)

# ------------------------------------------
# Cluster Summary
# ------------------------------------------

cluster_summary = df.groupby("Cluster").agg({
    "R": "mean",
    "F": "mean",
    "M": "mean",
    "Income": "mean",
    "Age": "mean"
}).round(2)

print("\nCluster Summary")
print(cluster_summary)

# ------------------------------------------
# Customer Count
# ------------------------------------------

customer_count = df["Cluster"].value_counts().sort_index()

print("\nCustomer Count")
print(customer_count)

cluster_summary["CustomerCount"] = customer_count

# ------------------------------------------
# Revenue Contribution
# ------------------------------------------

cluster_summary["Revenue"] = df.groupby("Cluster")["M"].sum()

total_revenue = cluster_summary["Revenue"].sum()

cluster_summary["RevenueContribution(%)"] = (
    cluster_summary["Revenue"] / total_revenue
) * 100

cluster_summary["RevenueContribution(%)"] = (
    cluster_summary["RevenueContribution(%)"].round(2)
)

# ------------------------------------------
# Assign Business Names
# ------------------------------------------

segment_names = {
    0: "High Value Customers",
    1: "Loyal Customers",
    2: "At Risk Customers",
    3: "New Customers",
    4: "Discount Lovers"
}

cluster_summary["SegmentName"] = (
    cluster_summary.index.map(segment_names)
)

print("\nCluster Profile")
print(cluster_summary)

# ------------------------------------------
# Save Report
# ------------------------------------------

cluster_summary.to_csv(
    "reports/segment_profile.csv"
)

print("\nSegment Profile Saved Successfully!")

# ------------------------------------------
# Customer Count Plot
# ------------------------------------------

plt.figure(figsize=(8,5))

customer_count.plot(
    kind="bar",
    color="skyblue"
)

plt.title("Customers in Each Segment")

plt.xlabel("Cluster")

plt.ylabel("Customer Count")

plt.grid(True)

plt.show()

# ------------------------------------------
# Revenue Plot
# ------------------------------------------

plt.figure(figsize=(8,5))

cluster_summary["Revenue"].plot(
    kind="bar",
    color="green"
)

plt.title("Revenue by Customer Segment")

plt.xlabel("Cluster")

plt.ylabel("Revenue")

plt.grid(True)

plt.show()

# ------------------------------------------
# Average Monetary Plot
# ------------------------------------------

plt.figure(figsize=(8,5))

cluster_summary["M"].plot(
    kind="bar",
    color="orange"
)

plt.title("Average Monetary Value")

plt.xlabel("Cluster")

plt.ylabel("Average Monetary")

plt.grid(True)

plt.show()

print("\nCustomer Segment Profiling Completed Successfully!")