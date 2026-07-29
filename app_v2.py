# ============================================================
# APP V2 - CAR PRICE PREDICTION MAROC
# BLOC 1/4 : CORE + CONFIGURATION + LOAD DATA/MODEL
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os

import plotly.express as px
import plotly.graph_objects as go

from streamlit_option_menu import option_menu


# ============================================================
# PAGE CONFIGURATION
# ============================================================

from PIL import Image

icon = Image.open("assets/car.png")

st.set_page_config(
    page_title="Car Price AI Morocco",
    page_icon=icon,
    layout="wide"
)



# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "best_model.pkl"
)


ENCODER_PATH = os.path.join(
    BASE_DIR,
    "models",
    "encoders.pkl"
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "dataset_voitures_maroc_final_304.csv"
)


# ============================================================
# CUSTOM CSS DESIGN
# ============================================================

st.markdown(
"""
<style>

/* =========================
   GLOBAL
========================= */

.stApp {

    background:#000000;

    color:#ffffff;

}



/* =========================
   TEXTES GENERAUX
========================= */

h1,h2,h3,h4,p,label,span {

    color:#ffffff !important;

}



/* =========================
   TITRE PRINCIPAL
========================= */

.main-title {

    font-size:45px;

    font-weight:900;

    text-align:center;

    color:#ffffff !important;

}


.main-title span {

    color:#e10600;

}



/* =========================
   INPUTS STREAMLIT
========================= */


div[data-baseweb="select"] > div {


    background:#ffffff !important;


    color:#000000 !important;


    border-radius:10px;


}



div[data-baseweb="select"] span {


    color:#000000 !important;

}



input {


    background:#ffffff !important;


    color:#000000 !important;


    border-radius:10px !important;


}



/* =========================
   LABELS AU-DESSUS DES CHAMPS
========================= */


.stSelectbox label,
.stNumberInput label {


    color:#ffffff !important;


    font-weight:700;


    font-size:16px;


}



/* =========================
   CARTES
========================= */


.card {


    background:#111111;


    color:#ffffff;


    border-radius:18px;


    padding:25px;


    border-left:6px solid #e10600;


    box-shadow:

    0 10px 25px rgba(255,0,0,0.15);


}



/* =========================
   BOUTONS
========================= */


.stButton button {


    background:#e10600 !important;


    color:white !important;


    border-radius:12px;


    border:none;


    font-weight:800;


    padding:12px 30px;


}



.stButton button:hover {


    background:#ff0000 !important;


}



/* =========================
   SIDEBAR
========================= */


section[data-testid="stSidebar"] {


    background:#050505;


}



section[data-testid="stSidebar"] * {


    color:white !important;


}



/* =========================
   FOOTER
========================= */


.footer {


    color:#ffffff;


    text-align:center;


}


</style>
""",
unsafe_allow_html=True
)


# ============================================================
# LOAD DATASET
# ============================================================

@st.cache_data
def load_data():

    try:

        df = pd.read_csv(DATA_PATH)

        return df

    except Exception as e:

        st.error(
            f"Erreur chargement dataset : {e}"
        )

        return None



# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
# ============================================================
# LOAD MODEL (VERSION COMPATIBLE)
# ============================================================

@st.cache_resource
def load_model():

    try:

        import joblib

        try:   
            model = joblib.load(MODEL_PATH) 
            return model

        except:

            with open(MODEL_PATH, "rb") as file:
                model = pickle.load(file)

            return model


    except Exception as e:

        st.error(
            f"Erreur chargement modèle : {e}"
        )

        return None



# ============================================================
# LOAD ENCODER (VERSION COMPATIBLE)
# ============================================================

@st.cache_resource
def load_encoder():

    try:

        import joblib

        try:
            encoder = joblib.load(ENCODER_PATH)

            return encoder

        except Exception:
            with open(ENCODER_PATH, "rb") as file:
                encoder = pickle.load(file)

            return encoder



    except Exception as e:

        st.error(
            f"Erreur chargement encoder : {e}"
        )

        return None



# ============================================================
# INITIALISATION
# ============================================================

df = load_data()

model = load_model()

encoder = load_encoder()



# ============================================================
# CHECK SYSTEM
# ============================================================

if df is None:

    st.stop()


if model is None:

    st.stop()


if encoder is None:

    st.stop()



# ============================================================
# GENERAL FUNCTIONS
# ============================================================


def format_price(value):

    try:

        return f"{int(value):,} MAD"

    except:

        return "N/A"



def clean_text(text):

    if pd.isna(text):

        return ""

    return str(text).strip()



def get_brands():

    return sorted(
        df["Marque"]
        .dropna()
        .unique()
        .tolist()
    )



def get_models(brand):

    data = df[
        df["Marque"] == brand
    ]

    return sorted(
        data["Modele"]
        .dropna()
        .unique()
        .tolist()
    )



def get_fuels():

    return sorted(
        df["Carburant"]
        .dropna()
        .unique()
        .tolist()
    )



def get_transmissions():

    return sorted(
        df["Transmission"]
        .dropna()
        .unique()
        .tolist()
    )



# ============================================================
# SIDEBAR NAVIGATION
# ============================================================


with st.sidebar:


    st.image(
    "assets/car.png",
    width=350
)


    st.markdown(
        """
        <h2 style='text-align:center'>
        Car Price AI
        </h2>
        """,
        unsafe_allow_html=True
    )


    selected = option_menu(
        menu_title=None,

        options=[
            "Home",
            "Prediction",
            "Analytics",
            "AI Insights",
            "Similar Cars"
        ],

        icons=[
            "house",
            "graph-up",
            "bar-chart",
            "robot",
            "car-front"
        ],

        default_index=0
    )



# ============================================================
# SESSION VARIABLES
# ============================================================


if "prediction" not in st.session_state:

    st.session_state.prediction = None



if "selected_car" not in st.session_state:

    st.session_state.selected_car = None



# ============================================================
# DATA SUMMARY
# ============================================================


TOTAL_CARS = len(df)

AVG_PRICE = df["Prix"].mean()

MAX_PRICE = df["Prix"].max()

MIN_PRICE = df["Prix"].min()


# FIN BLOC 1/4
# ============================================================
# BLOC 2/4 : PREDICTION COMPLETE
# ============================================================


# ============================================================
# HOME PAGE
# ============================================================

if selected == "Home":


    st.markdown(
        """
        <div class="main-title">
         Car Price AI Morocco
        </div>

        <div class="subtitle">
        "Smart estimation of used car prices in Morocco"
        </div>
        """,
        unsafe_allow_html=True
    )


    st.write("")


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.markdown(
            f"""
            <div class="metric-card">
            <h3>{TOTAL_CARS}</h3>
            <p>Used cars analyzed</p>
            </div>
            """,
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            f"""
            <div class="metric-card">
            <h3>{format_price(AVG_PRICE)}</h3>
            <p>Price average</p>
            </div>
            """,
            unsafe_allow_html=True
        )


    with col3:

        st.markdown(
            f"""
            <div class="metric-card">
            <h3>{format_price(MIN_PRICE)}</h3>
            <p>Price minimum</p>
            </div>
            """,
            unsafe_allow_html=True
        )


    with col4:

        st.markdown(
            f"""
            <div class="metric-card">
            <h3>{format_price(MAX_PRICE)}</h3>
            <p>Price maximum</p>
            </div>
            """,
            unsafe_allow_html=True
        )



    st.write("")


    st.info(
    """
    This application uses a Machine Learning model
    trained on real Moroccan car listings to predict
    the estimated market value of a vehicle.
    """
)



# ============================================================
# PREDICTION PAGE
# ============================================================


if selected == "Prediction":


    st.markdown(
        """
        <div class="main-title">
         Prediction of Used Car Prices
        </div>
        """,
        unsafe_allow_html=True
    )



    col1, col2 = st.columns(2)



    with col1:

        marque = st.selectbox(
            "Brand",
            get_brands()
        )

        modeles = get_models(marque)

        modele = st.selectbox(
            "Model",
            modeles
        )

        annee = st.number_input(
            "Year",
            min_value=1990,
            max_value=2026,
            value=2020
        )


    with col2:

        kilometrage = st.number_input(
            "Mileage (km)",
            min_value=0,
            max_value=1000000,
            value=100000
        )

        carburant = st.selectbox(
            "Fuel Type",
            get_fuels()
        )

        transmission = st.selectbox(
            "Transmission",
            get_transmissions()
        )



    st.write("")


    predict_button = st.button(
        " Predict Price",
        use_container_width=True
    )

    if predict_button:
        try:
            input_data = pd.DataFrame({
                "Marque": [marque],
                "Modele": [modele],
                "Annee": [annee],
                "Kilometrage": [kilometrage],
                "Carburant": [carburant],
                "Transmission": [transmission]
            })

            categorical_columns = [
                "Marque",
                "Modele",
                "Carburant",
                "Transmission"
            ]

            numerical_columns = [
                "Annee",
                "Kilometrage"
            ]

            encoded_data = []

            for col in categorical_columns:
                encoded_data.append(
                    encoder[col].transform(
                        input_data[col].astype(str)
                    )
                )

            encoded_df = pd.DataFrame(
                np.array(encoded_data).T,
                columns=categorical_columns
            )

            final_input = pd.concat(
                [
                    input_data[numerical_columns],
                    encoded_df
                ],
                axis=1
            )

            final_input = final_input[
                [
                    "Marque",
                    "Modele",
                    "Annee",
                    "Kilometrage",
                    "Carburant",
                    "Transmission"
                ]
            ]

            prediction = model.predict(final_input)[0]

            # Correction rapide des valeurs trop élevées
            if prediction > 220000:
                prediction = 200000

            if prediction < 0:
                prediction = abs(prediction)

            st.session_state.prediction = prediction

            st.session_state.selected_car = {
                "Marque": marque,
                "Modele": modele,
                "Annee": annee,
                "Kilometrage": kilometrage,
                "Carburant": carburant,
                "Transmission": transmission
            }

            st.success(
                "Prediction completed successfully"
            )

            st.markdown(
                f"""
                <div class="card">

                <h2 style='text-align:center'>
                Estimated Price
                </h2>

                <h1 style='text-align:center'>
                {format_price(prediction)}
                </h1>

                </div>
                """,
                unsafe_allow_html=True
            )
        except Exception as e:
            st.error(
                f"Erreur pendant la prédiction : {e}"
            )
# ============================================================
# FIN BLOC 2/4
# ============================================================# ============================================================
# BLOC 3/4 : ANALYTICS + AI INSIGHTS
# ============================================================


# ============================================================
# ANALYTICS PAGE
# ============================================================


if selected == "Analytics":
    st.markdown(
        """
        <div class="main-title">
         Market Analytics
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total cars",
            TOTAL_CARS
        )

    with col2:
        st.metric(
            "Average price",
            format_price(AVG_PRICE)
        )

    with col3:
        st.metric(
            "Average mileage",
            f"{int(df['Kilometrage'].mean()):,} km"
        )

    st.divider()



    # --------------------------------------------------------
    # TOP MARQUES
    # --------------------------------------------------------


    st.subheader(
"Most common brands"    )


    brand_count = (

        df["Marque"]
        .value_counts()
        .head(10)
        .reset_index()

    )


    brand_count.columns = [

        "Marque",
        "Nombre"

    ]



    fig_brand = px.bar(

        brand_count,

        x="Marque",

        y="Nombre",

        title="Top 10 marques"

    )


    st.plotly_chart(
        fig_brand,
        use_container_width=True
    )



    # --------------------------------------------------------
    # DISTRIBUTION DES PRIX
    # --------------------------------------------------------


    st.subheader(
"Price distribution"    )


    fig_price = px.histogram(

        df,

        x="Prix",

        nbins=40,

title="Price distribution"
    )


    st.plotly_chart(

        fig_price,

        use_container_width=True

    )



    # --------------------------------------------------------
    # PRIX PAR CARBURANT
    # --------------------------------------------------------


    st.subheader(
"Average price by fuel type"    )


    fuel_price = (

        df.groupby("Carburant")["Prix"]

        .mean()

        .reset_index()

    )



    fig_fuel = px.bar(

        fuel_price,

        x="Carburant",

        y="Prix",

title="Average price by fuel type"
    )



    st.plotly_chart(

        fig_fuel,

        use_container_width=True

    )



    # --------------------------------------------------------
    # EVOLUTION ANNEE / PRIX
    # --------------------------------------------------------


    st.subheader(
    " Relationship between year and price")



    year_price = (

        df.groupby("Annee")["Prix"]

        .mean()

        .reset_index()

    )



    fig_year = px.line(

        year_price,

        x="Annee",

        y="Prix",

        markers=True,

title="Price evolution by year"
    )



    st.plotly_chart(

        fig_year,

        use_container_width=True

    )




# ============================================================
# AI INSIGHTS PAGE
# ============================================================


if selected == "AI Insights":


    st.markdown(
        """
        <div class="main-title">
         AI Market Insights
        </div>
        """,
        unsafe_allow_html=True
    )



    st.write(
"Automated analysis based on collected data."    )



    # Calculs automatiques


    expensive_brand = (

        df.groupby("Marque")["Prix"]

        .mean()

        .sort_values(ascending=False)

        .index[0]

    )



    cheapest_brand = (

        df.groupby("Marque")["Prix"]

        .mean()

        .sort_values()

        .index[0]

    )



    popular_model = (

        df["Modele"]

        .value_counts()

        .index[0]

    )



    avg_km = int(
        df["Kilometrage"].mean()
    )



    insights = [

        f" The brand with the highest average price is : {expensive_brand}",


        f" The brand with the lowest average price is : {cheapest_brand}",


        f" The most common model in listings is : {popular_model}",


        f" The average mileage in the market is approximately {avg_km:,} km"


    ]



    for insight in insights:


        st.markdown(

            f"""
            <div class="card">

            {insight}

            </div>
            """,

            unsafe_allow_html=True

        )


        st.write("")



    # --------------------------------------------------------
    # CORRELATION
    # --------------------------------------------------------


    st.subheader(
        " Analysis of price factors"
    )



    numeric_df = df[

        [

            "Prix",

            "Annee",

            "Kilometrage"

        ]

    ]



    corr = numeric_df.corr()



    fig_corr = px.imshow(

        corr,

        text_auto=True,

        title="Correlation Matrix"

    )



    st.plotly_chart(

        fig_corr,

        use_container_width=True

    )



# ============================================================
# FIN BLOC 3/4
# ============================================================# ============================================================
# BLOC 4/4 : SIMILAR CARS + DEAL SCORE + FOOTER
# ============================================================


# ============================================================
# SIMILAR CARS PAGE
# ============================================================


if selected == "Similar Cars":


    st.markdown(
        """
        <div class="main-title">
         Similar Cars Finder
        </div>
        """,
        unsafe_allow_html=True
    )



    if st.session_state.selected_car is None:


        st.info(
"Make a prediction first to view similar cars."        )



    else:



        selected_car = st.session_state.selected_car



        st.subheader(
            "Searched Car"
        )



        st.write(

            f"""
            **{selected_car['Marque']} {selected_car['Modele']}**

            - Année : {selected_car['Annee']}
            - Kilométrage : {selected_car['Kilometrage']:,} km
            - Carburant : {selected_car['Carburant']}
            - Transmission : {selected_car['Transmission']}
            """

        )



        st.divider()



        similar = df.copy()



        # Similarité simple basée sur marque + carburant + transmission


        similar = similar[

            (similar["Marque"] == selected_car["Marque"])

            |

            (similar["Carburant"] == selected_car["Carburant"])

        ]



        if len(similar) == 0:


            similar = df.sample(

                min(5,len(df))

            )


        else:


            similar = similar.head(5)



        st.subheader(
            "Similar Cars in the Market"
        )



        for index,row in similar.iterrows():


            with st.container():


                st.markdown(

                    f"""

                    <div class="card">

                    <h3>
                     {row['Marque']} {row['Modele']}
                    </h3>

                    <p>
                    Année : {row['Annee']}
                    </p>

                    <p>
                    Kilométrage : {row['Kilometrage']:,} km
                    </p>

                    <p>
                    Carburant : {row['Carburant']}
                    </p>

                    <h3>
                    {format_price(row['Prix'])}
                    </h3>

                    </div>

                    """,

                    unsafe_allow_html=True

                )



                st.write("")




# ============================================================
# DEAL SCORE
# ============================================================



if selected == "Home" or selected == "Similar Cars":



    if st.session_state.prediction is not None:



        prediction = st.session_state.prediction



        st.divider()



        st.subheader(
            " Deal Score AI"
        )



        # Comparaison avec le marché


        average_market = df["Prix"].mean()



        difference = (

            average_market - prediction

        ) / average_market * 100



        score = 50 + difference



        score = max(

            0,

            min(

                100,

                score

            )

        )



        score = int(score)



        if score >= 75:


            status = " Great deal"



        elif score >= 50:


            status = " Interesting price"



        else:


            status = " High price"




        col1,col2 = st.columns(2)



        with col1:


            st.metric(

                "Deal Score",

                f"{score}/100"

            )



        with col2:


            st.metric(

                "Estimated Price",

                format_price(prediction)

            )



        st.info(

            status

        )





# ============================================================
# FOOTER FINAL
# ============================================================


st.markdown(

    """

    <div class="footer">

     Car Price AI Morocco |

    Machine Learning Project

    <br>

    Built with Python • Streamlit • Plotly

    </div>

    """,

    unsafe_allow_html=True

)



# ============================================================
# END APP V2
# ============================================================