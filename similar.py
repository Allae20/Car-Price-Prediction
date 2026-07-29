import pandas as pd

def similar_cars(df, marque, modele, n=5):

    cars = df[
        (df["Marque"] == marque) &
        (df["Modele"] == modele)
    ]

    return cars.head(n)