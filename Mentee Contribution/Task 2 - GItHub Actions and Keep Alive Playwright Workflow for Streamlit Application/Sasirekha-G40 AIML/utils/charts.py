import plotly.express as px


# --------------------------------------------------
# Churn Distribution
# --------------------------------------------------
def churn_chart(df):

    data = (
        df
        .group_by("Churn")
        .len()
        .sort("Churn")
        .to_pandas()
    )

    data["Churn"] = data["Churn"].replace(
        {
            0: "Retained",
            1: "Churned"
        }
    )

    fig = px.bar(
        data,
        x="Churn",
        y="len",
        color="Churn",
        text="len",
        title="Customer Churn Distribution"
    )

    fig.update_layout(
        xaxis_title="Customer Status",
        yaxis_title="Number of Customers"
    )

    return fig


# --------------------------------------------------
# Gender Distribution
# --------------------------------------------------
def gender_chart(df):

    data = (
        df
        .group_by("Gender")
        .len()
        .to_pandas()
    )

    fig = px.pie(
        data,
        names="Gender",
        values="len",
        hole=0.45,
        title="Gender Distribution"
    )

    return fig


# --------------------------------------------------
# Preferred Payment Mode
# --------------------------------------------------
def payment_chart(df):

    data = (
        df
        .group_by("PreferredPaymentMode")
        .len()
        .sort("len", descending=True)
        .to_pandas()
    )

    fig = px.bar(
        data,
        x="PreferredPaymentMode",
        y="len",
        color="PreferredPaymentMode",
        text="len",
        title="Preferred Payment Mode"
    )

    fig.update_layout(
        xaxis_title="Payment Mode",
        yaxis_title="Customers"
    )

    return fig


# --------------------------------------------------
# Customers by City Tier
# --------------------------------------------------
def city_chart(df):

    data = (
        df
        .group_by("CityTier")
        .len()
        .sort("CityTier")
        .to_pandas()
    )

    fig = px.bar(
        data,
        x="CityTier",
        y="len",
        color="CityTier",
        text="len",
        title="Customers by City Tier"
    )

    fig.update_layout(
        xaxis_title="City Tier",
        yaxis_title="Customers"
    )

    return fig


# --------------------------------------------------
# Satisfaction Score
# --------------------------------------------------
def satisfaction_chart(df):

    data = (
        df
        .group_by("SatisfactionScore")
        .len()
        .sort("SatisfactionScore")
        .to_pandas()
    )

    fig = px.line(
        data,
        x="SatisfactionScore",
        y="len",
        markers=True,
        title="Customer Satisfaction Score"
    )

    fig.update_layout(
        xaxis_title="Satisfaction Score",
        yaxis_title="Customers"
    )

    return fig


# --------------------------------------------------
# Cashback Distribution
# --------------------------------------------------
def cashback_chart(df):

    fig = px.histogram(
        df.to_pandas(),
        x="CashbackAmount",
        nbins=30,
        title="Cashback Distribution"
    )

    fig.update_layout(
        xaxis_title="Cashback Amount",
        yaxis_title="Frequency"
    )

    return fig