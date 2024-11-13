import fused
import streamlit as st
import asyncio
import pydeck as pdk
from requests.models import PreparedRequest

st.sidebar.header("Day 8 - Data (HDX)")
st.title("2021 Humanitarian Developlment Index per country")
st.markdown(
    """
    This is a map showing the 2021 Humanitarian Development Index from the [Human Development Data](https://data.humdata.org/dataset/human-development-data) dataset hosted on HDX.
    """
)

deck = st.empty()
percentage_slider = st.slider("Highest percentage ranked of countries", 0, 100, 5)

view_state = pdk.ViewState(
    latitude=0,
    longitude=0,
    zoom=2,
    pitch=0
)

initial_deck = pdk.Deck(
    initial_view_state=view_state,
    map_style='mapbox://styles/mapbox/light-v9'
)
deck.pydeck_chart(initial_deck)

@st.cache_resource
def fetch_data():
    gdf = fused.run("fsh_49hXAtlrDDHr2MFvLBHlLW")
    return gdf

gdf = fetch_data()

# Slicing in frontend, 
highest_rank = int((gdf.shape[0] * percentage_slider) / 100)
gdf = gdf[gdf['hdi_rank_2021'] < highest_rank]

geojson_layer = pdk.Layer(
    'GeoJsonLayer',
    gdf,
    opacity=0.8,
    stroked=True,
    filled=True,
    extruded=False,
    wire_frame=True,
    get_fill_color=[0, 250, 0],
    get_line_color=[0, 0, 0],
    get_line_width=2,
)

updated_deck = pdk.Deck(
    layers=[geojson_layer],
    initial_view_state=view_state,
    map_style='mapbox://styles/mapbox/light-v9'
)

# Display the updated map in Streamlit
deck.pydeck_chart(updated_deck)

st.write(
    """
    This app was made by [Max Lenormand](https://www.linkedin.com/in/maxime-lenormand-b94640107/)
    """
)