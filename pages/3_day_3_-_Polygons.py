# This is a streamlit app code
import numpy as np
import pandas as pd
import streamlit as st

# Us this datapoints: https://www.fused.io/workbench/catalog/FEMA_Buildings_US-ae1feed0-215a-42b5-8cf4-d95f5c1216dc
st.sidebar.header("Day 3 - Polygons")

st.title("Day 3 - Explore Building Size Distributions")
st.write(
    """
    This app allows you to look at the distribution of the largest buildings
    """
)

bbox=[-122.449, 37.781, -122.341, 37.818]


#sina.py
import json
import fused
import streamlit as st
import asyncio
import pydeck as pdk
import pydeck_carto as pdkc
from requests.models import PreparedRequest

import geopandas
import folium
from streamlit_folium import st_folium


@st.cache_resource
def fetch_data(bbox):
    gdf = fused.run("UDF_FEMA_Buildings_US", bbox=bbox)
    return gdf
gdf = fetch_data(bbox)#.sample(10_000)

st.write(gdf.head())
centroid_x = gdf.centroid.x.mean()
centroid_y = gdf.centroid.y.mean()

largest_area = gdf['SQMETERS'].max()
st.write(f"{largest_area=}")

deck = st.empty()

percentage_slider = st.slider("Buidling area percentile to keep", 0, 100, 5)
area_threshold = percentage_slider * largest_area / 100

gdf = gdf[gdf["SQMETERS"] > area_threshold]
st.write(f"{gdf.shape=}")

view_state = pdk.ViewState(
    latitude=centroid_y,
    longitude=centroid_x,
    zoom=14,
    pitch=0
)

initial_deck = pdk.Deck(
    initial_view_state=view_state,
    map_style='mapbox://styles/mapbox/light-v9'
)
deck.pydeck_chart(initial_deck)

color = pdkc.styles.color_categories("OCC_CLS", ["Assembly",
        "Commercial",
        "Utility and Misc",
        "Residential",
        "Industrial",
        "Education",
        "Government"], "Bold",[100,100,0])
as_geojson = json.loads(gdf[['geometry', 'OCC_CLS']].to_json())
geojson_layer = pdk.Layer(
    'GeoJsonLayer',
    as_geojson,
    opacity=0.8,
    stroked=True,
    filled=True,
    extruded=False,
    wire_frame=False,
    get_fill_color=color,
    get_line_color=color,
    get_line_width=2,
)

updated_deck = pdk.Deck(
    layers=[geojson_layer],
    initial_view_state=view_state,
    map_style='mapbox://styles/mapbox/light-v9'
)

# Display the updated map in Streamlit
deck.pydeck_chart(updated_deck)