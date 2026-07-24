import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Analytics0" \
"")

st.title('Analytics')

new_df = pd.read_csv('datasets/data_viz1.csv')
import pickle

sector_feature_list = pickle.load(
    open('datasets/sector_features.pkl', 'rb')
)
sector_feature_dict = dict(sector_feature_list)


group_df = new_df.groupby('sector').mean(numeric_only=True)[['price','price_per_sqft','built_up_area','latitude','longitude']]

st.header('Sector Price per Sqft Geomap')
fig = px.scatter_mapbox(group_df, lat="latitude", lon="longitude", color="price_per_sqft", size='built_up_area',
                  color_continuous_scale=px.colors.cyclical.IceFire, zoom=10,
                  mapbox_style="open-street-map",width=1200,height=700,hover_name=group_df.index, labels={"price_per_sqft": "Price/sqft"})

st.plotly_chart(fig,use_container_width=True)

st.header('Features Wordcloud')

import re
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load sector-wise features
sector_feature_dict = pickle.load(
    open('datasets/sector_features.pkl', 'rb')
)
sector_feature_dict = dict(sector_feature_list)
# Sort sectors numerically: Sector 1, Sector 2, Sector 3 ...
import re

sector_options = sorted(
    sector_feature_dict.keys(),
    key=lambda x: (
        0 if re.search(r'\d+', str(x)) else 1,
        int(re.search(r'\d+', str(x)).group()) if re.search(r'\d+', str(x)) else float('inf'),
        str(x)
    )
)
# Add overall at the end
# sector_options.append('overall')
sector_options.insert(0, 'overall')

# Dropdown
selected_sector = st.selectbox(
    'Select Sector',
    sector_options
)

# Features for selected sector
if selected_sector == 'overall':

    features = []

    for sector_features in sector_feature_dict.values():
        features.extend(sector_features)

else:

    features = sector_feature_dict[selected_sector]

# Generate WordCloud
text = " ".join(features)

wordcloud = WordCloud(
    width=800,
    height=800,
    background_color='black',
    min_font_size=10
).generate(text)

fig, ax = plt.subplots(figsize=(8, 8))

ax.imshow(wordcloud, interpolation='bilinear')
ax.axis('off')

st.pyplot(fig)
st.header('Area Vs Price')

# for piechart
property_type = st.selectbox('Select Property Type', ['flat','house'])

if property_type == 'house':
    fig1 = px.scatter(new_df[new_df['property_type'] == 'house'], x="built_up_area", y="price", color="bedRoom", title="Area Vs Price")

    st.plotly_chart(fig1, use_container_width=True)
else:
    fig1 = px.scatter(new_df[new_df['property_type'] == 'flat'], x="built_up_area", y="price", color="bedRoom",
                      title="Area Vs Price")

    st.plotly_chart(fig1, use_container_width=True)

st.header('BHK Pie Chart')

import re

# Sort sectors numerically
sector_options = sorted(
    new_df['sector'].dropna().unique().tolist(),
    key=lambda x: (
        int(re.search(r'\d+', str(x)).group())
        if re.search(r'\d+', str(x))
        else float('inf')
    )
)

# Add overall at the end
# sector_options.append('overall')
sector_options.insert(0, 'overall')

selected_sector = st.selectbox(
    'Select Sector',
    sector_options,
    key='pie_sector'
)

if selected_sector == 'overall':

    fig2 = px.pie(
        new_df,
        names='bedRoom',
        title='BHK Distribution'
    )

else:

    fig2 = px.pie(
        new_df[new_df['sector'] == selected_sector],
        names='bedRoom',
        title=f'BHK Distribution - {selected_sector}'
    )

st.plotly_chart(fig2, use_container_width=True)

# sector_options = new_df['sector'].unique().tolist()
# sector_options.insert(0,'overall')

# selected_sector = st.selectbox('Select Sector', sector_options)

# if selected_sector == 'overall':

#     fig2 = px.pie(new_df, names='bedRoom')

#     st.plotly_chart(fig2, use_container_width=True)
# else:

#     fig2 = px.pie(new_df[new_df['sector'] == selected_sector], names='bedRoom')

#     st.plotly_chart(fig2, use_container_width=True)

st.header('Side by Side BHK price comparison')

fig3 = px.box(new_df[new_df['bedRoom'] <= 4], x='bedRoom', y='price', title='BHK Price Range')

st.plotly_chart(fig3, use_container_width=True)


st.header('Side by Side Distplot for property type')

fig3 = plt.figure(figsize=(10, 4))
sns.histplot(new_df[new_df['property_type'] == 'house']['price'],label='house')
sns.histplot(new_df[new_df['property_type'] == 'flat']['price'], label='flat')
plt.legend()
st.pyplot(fig3)