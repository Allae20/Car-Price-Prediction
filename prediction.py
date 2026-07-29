import pandas as pd

def predict_price(
    model,
    encoders,
    marque,
    modele,
    annee,
    kilometrage,
    carburant,
    transmission,
):

    marque_encoded = encoders["Marque"].transform([marque])[0]
    modele_encoded = encoders["Modele"].transform([modele])[0]
    carburant_encoded = encoders["Carburant"].transform([carburant])[0]
    transmission_encoded = encoders["Transmission"].transform([transmission])[0]

    features = pd.DataFrame({
        "Marque": [marque_encoded],
        "Modele": [modele_encoded],
        "Annee": [annee],
        "Kilometrage": [kilometrage],
        "Carburant": [carburant_encoded],
        "Transmission": [transmission_encoded]
    })

    prediction = model.predict(features)[0]

    return prediction