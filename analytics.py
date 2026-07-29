import plotly.express as px

def price_distribution(df):
    fig = px.histogram(
        df,
        x="Prix",
        nbins=30,
        title="Price Distribution",
        color_discrete_sequence=["#1f77b4"]
    )
    return fig


def average_price_by_brand(df):
    brand_df = (
        df.groupby("Marque")["Prix"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        brand_df,
        x="Marque",
        y="Prix",
        title="Top 10 Brands by Average Price"
    )

    return fig