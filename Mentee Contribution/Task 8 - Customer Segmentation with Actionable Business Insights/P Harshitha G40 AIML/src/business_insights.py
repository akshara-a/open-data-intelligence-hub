"""
Business Insights Module
=========================
Derives actionable business recommendations from the customer segments
and writes a markdown report to outputs/business_recommendations.md
"""

import pandas as pd
# pyrefly: ignore [missing-import]
import numpy as np
import os


SEGMENT_STRATEGIES = {
    "High-Value Loyal Customers": {
        "icon": "👑",
        "description": (
            "Customers with high purchase frequency, high total spending, "
            "recent purchases, and high average order value."
        ),
        "actions": [
            "Offer exclusive loyalty rewards and VIP membership benefits.",
            "Provide early access to new product launches.",
            "Send personalised thank-you campaigns to reinforce brand loyalty.",
            "Avoid over-discounting - these customers already show strong purchase intent.",
            "Upsell premium or complementary products to increase lifetime value.",
        ],
        "kpi": "Increase repeat purchase rate and average order value.",
    },
    "New and Promising Customers": {
        "icon": "🌱",
        "description": (
            "Recently acquired customers with low-to-medium purchase history "
            "but good early engagement signals."
        ),
        "actions": [
            "Send personalised onboarding emails with product recommendations.",
            "Offer a welcome discount on the second purchase to build habit.",
            "Highlight popular and best-selling products to guide exploration.",
            "Enrol in a new-customer nurture sequence (3-5 touch-points in 30 days).",
            "Collect feedback via survey to understand first-purchase experience.",
        ],
        "kpi": "Increase second-purchase conversion rate within 30 days.",
    },
    "Discount-Driven Customers": {
        "icon": "🏷️",
        "description": (
            "Customers who primarily purchase during promotions, with high discount "
            "usage and moderate purchase frequency."
        ),
        "actions": [
            "Send targeted limited-time promotional offers and flash sales.",
            "Bundle products to increase basket size while maintaining perceived value.",
            "Gradually reduce discount depth over time to improve margins.",
            "Avoid giving unnecessary discounts outside campaign periods.",
            "Test value-based messaging (quality, features) to reduce price sensitivity.",
        ],
        "kpi": "Improve margin per order while sustaining purchase frequency.",
    },
    "At-Risk Customers": {
        "icon": "⚠️",
        "description": (
            "Previously active customers with increasing days since last purchase, "
            "declining engagement, but moderate/high historical spending."
        ),
        "actions": [
            "Run automated re-engagement email campaigns ('We miss you' series).",
            "Offer a personalised come-back incentive based on purchase history.",
            "Request feedback on what caused them to stop - exit survey.",
            "Highlight new arrivals or improvements since their last visit.",
            "Set a 60-day win-back window; if no purchase, consider lower-cost channel.",
        ],
        "kpi": "Reactivate at least 20% of at-risk customers within 60 days.",
    },
    "Low-Engagement Customers": {
        "icon": "💤",
        "description": (
            "Customers with low purchase frequency, low total spending, "
            "limited website activity, and long purchase intervals."
        ),
        "actions": [
            "Use low-cost email campaigns - avoid expensive paid retargeting.",
            "Promote entry-level or lower-priced products to lower the commitment barrier.",
            "Test whether SMS or push notifications outperform email for this group.",
            "Analyse whether this segment should remain a marketing priority.",
            "Consider sunsetting persistent non-responders to reduce campaign costs.",
        ],
        "kpi": "Identify the subset worth retaining vs. sunsetting to optimise spend.",
    },
}


def _get_strategy(segment_name):
    """Return the closest strategy for the given segment name."""
    for key, val in SEGMENT_STRATEGIES.items():
        if key.lower() in segment_name.lower() or segment_name.lower() in key.lower():
            return key, val
    # Default fallback
    return segment_name, {
        "icon": "📊",
        "description": "A distinct customer group identified by the clustering model.",
        "actions": [
            "Analyse the segment characteristics carefully.",
            "Design targeted campaigns based on key behavioural drivers.",
            "Monitor engagement and purchase rates over time.",
        ],
        "kpi": "Establish baseline KPIs and set improvement targets.",
    }


def generate_recommendations(segment_profile, segment_names):
    """
    Generate a structured recommendation dictionary per segment.
    """
    recommendations = {}
    for cluster_id in segment_profile.index:
        seg_name = segment_names.get(cluster_id, f"Segment {cluster_id}")
        strategy_name, strategy = _get_strategy(seg_name)
        row = segment_profile.loc[cluster_id]

        recommendations[cluster_id] = {
            "cluster_id":     cluster_id,
            "segment_name":   seg_name,
            "strategy_name":  strategy_name,
            "icon":           strategy["icon"],
            "description":    strategy["description"],
            "customer_count": int(row.get('CustomerCount', 0)),
            "avg_spending":   float(row.get('TotalSpending', 0)),
            "avg_frequency":  float(row.get('PurchaseFrequency', 0)),
            "avg_recency":    float(row.get('DaysSinceLastPurchase', 0)),
            "avg_rating":     float(row.get('CustomerRating', 0)),
            "avg_discount":   float(row.get('DiscountUsage', 0)),
            "revenue_pct":    float(row.get('RevenueContribution%', 0)),
            "total_revenue":  float(row.get('TotalRevenue', 0)),
            "actions":        strategy["actions"],
            "kpi":            strategy["kpi"],
        }
    return recommendations


def write_markdown_report(recommendations, output_path):
    """Write the business recommendations to a markdown file."""
    lines = []
    lines.append("# Customer Segmentation - Business Recommendations Report\n")
    lines.append("> Generated automatically from K-Means clustering results.\n\n")
    lines.append("---\n\n")

    # Executive summary table
    lines.append("## Executive Summary\n\n")
    lines.append("| Cluster | Segment | Customers | Avg Spending | Revenue % | Avg Rating |\n")
    lines.append("|---------|---------|-----------|-------------|-----------|------------|\n")
    for cid, rec in recommendations.items():
        lines.append(
            f"| {cid} | {rec['icon']} {rec['segment_name']} "
            f"| {rec['customer_count']:,} "
            f"| ${rec['avg_spending']:,.0f} "
            f"| {rec['revenue_pct']:.1f}% "
            f"| {rec['avg_rating']:.2f} |\n"
        )
    lines.append("\n---\n\n")

    # Segment details
    lines.append("## Segment Profiles & Recommendations\n\n")
    for cid, rec in recommendations.items():
        lines.append(f"### {rec['icon']} Cluster {cid}: {rec['segment_name']}\n\n")
        lines.append(f"**Description:** {rec['description']}\n\n")

        # Characteristics table
        lines.append("#### Key Characteristics\n\n")
        lines.append("| Metric | Value |\n")
        lines.append("|--------|-------|\n")
        lines.append(f"| Number of Customers | {rec['customer_count']:,} |\n")
        lines.append(f"| Average Total Spending | ${rec['avg_spending']:,.2f} |\n")
        lines.append(f"| Average Purchase Frequency | {rec['avg_frequency']:.1f} |\n")
        lines.append(f"| Avg Days Since Last Purchase | {rec['avg_recency']:.1f} days |\n")
        lines.append(f"| Average Customer Rating | {rec['avg_rating']:.2f} / 5.0 |\n")
        lines.append(f"| Avg Discount Usage | {rec['avg_discount'] * 100:.1f}% |\n")
        lines.append(f"| Revenue Contribution | {rec['revenue_pct']:.1f}% |\n")
        lines.append(f"| Total Revenue | ${rec['total_revenue']:,.0f} |\n\n")

        # Actions
        lines.append("#### Recommended Actions\n\n")
        for i, action in enumerate(rec['actions'], 1):
            lines.append(f"{i}. {action}\n")
        lines.append("\n")

        # KPI
        lines.append(f"**Target KPI:** {rec['kpi']}\n\n")
        lines.append("---\n\n")

    # Key insights section
    recs_list = list(recommendations.values())
    if recs_list:
        highest_rev = max(recs_list, key=lambda r: r['total_revenue'])
        lowest_recency = min(recs_list, key=lambda r: r['avg_recency'])
        highest_discount = max(recs_list, key=lambda r: r['avg_discount'])
        highest_churn = max(recs_list, key=lambda r: r['avg_recency'])

        lines.append("## Key Business Insights\n\n")
        lines.append(
            f"- 💰 **Highest Revenue Segment:** {highest_rev['icon']} {highest_rev['segment_name']} "
            f"contributing **{highest_rev['revenue_pct']:.1f}%** of total revenue. "
            f"Prioritise loyalty programmes for this group.\n"
        )
        lines.append(
            f"- 🔁 **Most Recent Buyers:** {lowest_recency['icon']} {lowest_recency['segment_name']} "
            f"purchased on average **{lowest_recency['avg_recency']:.0f} days** ago - "
            f"great target for cross-sell campaigns.\n"
        )
        lines.append(
            f"- ⚠️ **Highest Churn Risk:** {highest_churn['icon']} {highest_churn['segment_name']} "
            f"with **{highest_churn['avg_recency']:.0f} days** since last purchase - "
            f"activate re-engagement campaigns immediately.\n"
        )
        lines.append(
            f"- 🏷️ **Most Discount-Sensitive:** {highest_discount['icon']} {highest_discount['segment_name']} "
            f"uses discounts in **{highest_discount['avg_discount'] * 100:.1f}%** of purchases - "
            f"use targeted promotions but protect margins.\n"
        )

    lines.append("\n---\n")
    lines.append("*Report generated by the Customer Segmentation ML Pipeline.*\n")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f"Saved: {output_path}")


def run_business_insights(segment_profile, segment_names, outputs_dir):
    """
    Run the business insights module.
    Returns the recommendations dictionary.
    """
    os.makedirs(outputs_dir, exist_ok=True)

    print("\n" + "=" * 60)
    print("BUSINESS INSIGHTS & RECOMMENDATIONS")
    print("=" * 60)

    recommendations = generate_recommendations(segment_profile, segment_names)

    output_path = os.path.join(outputs_dir, 'business_recommendations.md')
    write_markdown_report(recommendations, output_path)

    print("\nBusiness insights complete!")
    print(f"Report saved to: {output_path}")

    return recommendations


if __name__ == "__main__":
    import json
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    segments_path = os.path.join(base_dir, "outputs", "customer_segments.csv")
    outputs_dir   = os.path.join(base_dir, "outputs")

    if os.path.exists(segments_path):
        segment_profile = pd.read_csv(segments_path, index_col=0)
        # Reconstruct segment_names from SegmentName column
        if 'SegmentName' in segment_profile.columns:
            segment_names = segment_profile['SegmentName'].to_dict()
        else:
            segment_names = {i: f"Segment {i}" for i in segment_profile.index}
        run_business_insights(segment_profile, segment_names, outputs_dir)
    else:
        print("Run the full pipeline first (app.py) to generate segment profiles.")
