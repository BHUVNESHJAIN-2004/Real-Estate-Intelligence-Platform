import streamlit as st
import pickle 
import pandas as pd
import numpy as np


import os
import gdown
import pickle

import sklearn
st.set_page_config(
    page_title="Price prediction"
)   
# import dataframe
with open('df.pkl','rb') as file :
    df = pickle.load(file)

import os
import gdown
import pickle

MODEL_PATH = "pipeline.pkl"

if not os.path.exists(MODEL_PATH):

    file_id = "1SOtHi9sbSr1HfwDiTunr2POUyX4vV8KP"

    gdown.download(
        f"https://drive.google.com/uc?id={file_id}",
        MODEL_PATH,
        quiet=False
    )

with open(MODEL_PATH, "rb") as f:
    pipeline = pickle.load(f)

# st.dataframe(df)

st.header('Enter your inputs')


# property type
Property_type = st.selectbox('Property Type',['flat','house'])

# sector
sector = st.selectbox('Sector',sorted(df['sector'].unique().tolist()))

# bedroom
bedroom = float(st.selectbox('Number of Bedroom',sorted(df['bedRoom'].unique().tolist()))) # because selectox box output is text

# bathroom
bathroom = float(st.selectbox('Number of Bathroom',sorted(df['bathroom'].unique().tolist())))

# balcony
balcony = st.selectbox('Balconies',sorted(df['balcony'].unique().tolist()))

# property age
Property_age = st.selectbox('Property Age',sorted(df['agePossession'].unique().tolist()))

# area
Built_up_area = float(st.number_input("Built up Area"))

# servant room (1->yes,0->no)
servant_room = float(st.selectbox('Servant room',[0.0,1.0]))

# store room (1->yes,0->no)
store_room = float(st.selectbox('Store room',[0.0,1.0]))

# furnishing (full,semi,no)
furnishing_type = st.selectbox('Furnishing Type',sorted(df['furnishing_type'].unique().tolist()))

# luxury (high,mid,low)
luxury_category = st.selectbox('Luxury Category',sorted(df['luxury_category'].unique().tolist()))

# floor(low,mid,high)
floor_category = st.selectbox('Floor Caregory Age',sorted(df['floor_category'].unique().tolist()))

# button to submit form

if st.button('Predict'):

    # form a dataframe
    data = [[Property_type, sector, bedroom, bathroom,balcony, Property_age, Built_up_area, servant_room, store_room, furnishing_type, luxury_category, floor_category]]
    columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
       'agePossession', 'built_up_area', 'servant room', 'store room',
       'furnishing_type', 'luxury_category', 'floor_category']
    one_df = pd.DataFrame(data, columns=columns)
    base_price = np.expm1(pipeline.predict(one_df))[0]
    low = base_price-0.22
    high = base_price+0.22
    st.text("The price of the {} is between {}cr  and  {}cr".format(Property_type,round(low,2),round(high,2)))

    