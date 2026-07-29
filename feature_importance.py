import pandas as pd
import plotly.express as px

def feature_importance(model):

    importance = pd.DataFrame({
        "Feature": [
            "Brand",
            "Model",
            "Year",
            "Mileage",
            "Fuel",
            "Transmission"
        ],
        "Importance": model.feature_importances_
    })

    importance = importance.sort_values(
        "Importance",
        ascending=False
    )

    fig = px.bar(
        importance,
        x="Importance",
        y="Feature",
        orientation="h",
        title="Feature Importance"
    )

    return fig