import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import gdown
import sklearn

st.set_page_config(
    page_title="Price prediction"
)

# Load dataframe
with open('df.pkl', 'rb') as file:
    df = pickle.load(file)

# ---------------- MODEL LOADING ---------------- #

MODEL_PATH = "pipeline.pkl"
FILE_ID = "1SOtHi9sbSr1HfwDiTunr2POUyX4vV8KP"

if not os.path.exists(MODEL_PATH):
    st.write("Downloading model...")

    gdown.download(
        f"https://drive.google.com/uc?id={FILE_ID}",
        MODEL_PATH,
        quiet=False
    )

# Debug information
# st.write("Scikit-learn version:", sklearn.__version__)

# if os.path.exists(MODEL_PATH):
#     st.write(
#         "Downloaded file size:",
#         round(os.path.getsize(MODEL_PATH) / (1024 * 1024), 2),
#         "MB"
    # )

try:
    with open(MODEL_PATH, "rb") as f:
        pipeline = pickle.load(f)

except Exception as e:
    st.error(f"Error loading model: {e}")
    raise

# ---------------- UI ---------------- #

st.header('Enter your inputs')

Property_type = st.selectbox(
    'Property Type',
    ['flat', 'house']
)

sector = st.selectbox(
    'Sector',
    sorted(df['sector'].unique().tolist())
)

bedroom = float(
    st.selectbox(
        'Number of Bedroom',
        sorted(df['bedRoom'].unique().tolist())
    )
)

bathroom = float(
    st.selectbox(
        'Number of Bathroom',
        sorted(df['bathroom'].unique().tolist())
    )
)

balcony = st.selectbox(
    'Balconies',
    sorted(df['balcony'].unique().tolist())
)

Property_age = st.selectbox(
    'Property Age',
    sorted(df['agePossession'].unique().tolist())
)

Built_up_area = float(
    st.number_input("Built up Area")
)

servant_room = float(
    st.selectbox(
        'Servant room',
        [0.0, 1.0]
    )
)

store_room = float(
    st.selectbox(
        'Store room',
        [0.0, 1.0]
    )
)

furnishing_type = st.selectbox(
    'Furnishing Type',
    sorted(df['furnishing_type'].unique().tolist())
)

luxury_category = st.selectbox(
    'Luxury Category',
    sorted(df['luxury_category'].unique().tolist())
)

floor_category = st.selectbox(
    'Floor Category',
    sorted(df['floor_category'].unique().tolist())
)

if st.button('Predict'):

    data = [[
        Property_type,
        sector,
        bedroom,
        bathroom,
        balcony,
        Property_age,
        Built_up_area,
        servant_room,
        store_room,
        furnishing_type,
        luxury_category,
        floor_category
    ]]

    columns = [
        'property_type',
        'sector',
        'bedRoom',
        'bathroom',
        'balcony',
        'agePossession',
        'built_up_area',
        'servant room',
        'store room',
        'furnishing_type',
        'luxury_category',
        'floor_category'
    ]

    one_df = pd.DataFrame(data, columns=columns)

    base_price = np.expm1(
        pipeline.predict(one_df)
    )[0]

    low = base_price - 0.22
    high = base_price + 0.22

    st.success(
        f"The price of the {Property_type} is between "
        f"{round(low, 2)} Cr and {round(high, 2)} Cr"
    )