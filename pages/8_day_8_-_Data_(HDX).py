import fused
import streamlit as st
import asyncio
import pydeck as pdk
from requests.models import PreparedRequest

import geopandas
import folium
from streamlit_folium import st_folium

st.sidebar.header("Day 8 - Data (HDX)")
st.title("2021 Humanitarian Developlment Index per country")
st.markdown(
    """
    This is a map showing the 2021 Humanitarian Development Index from the [Human Development Data](https://data.humdata.org/dataset/human-development-data) dataset hosted on HDX.
    """
)

percentage_slider = st.slider("Highest percentage ranked of countries", 0, 100, 5)
st.write(f"Slider value: {percentage_slider=}")

view_state = pdk.ViewState(
    latitude=0,
    longitude=0,
    zoom=2,
    pitch=0
)

@st.cache_resource
def fetch_data(percent = percentage_slider):
    gdf = fused.run("fsh_49hXAtlrDDHr2MFvLBHlLW", highest_percentage=percent)
    return gdf

gdf = fetch_data(percentage_slider)
st.write(f"Recieved gdf: {gdf.shape=}")

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

deck = pdk.Deck(
    layers=[geojson_layer],
    initial_view_state=view_state,
    map_style='mapbox://styles/mapbox/light-v9'
)

# Display the map in Streamlit
st.pydeck_chart(deck)