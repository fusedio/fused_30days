# This is a streamlit app code
import numpy as np
import pandas as pd
import streamlit as st

# Us this datapoints: https://www.fused.io/workbench/catalog/FEMA_Buildings_US-ae1feed0-215a-42b5-8cf4-d95f5c1216dc
# st.sidebar.header("Day 3 - Polygons")

st.title("Day 3 - Explore Building Size Distributions")
st.write(
    """
    This app allows you to look at the distribution of the largest buildings!

    We're using data from Oak Ridge National Laboratory and FEMA. [Find more info here](https://tech.marksblogg.com/ornl-fema-buildings.html)
    """
)

bbox=[-122.449, 37.781, -122.341, 37.818]

import json
import fused
import streamlit as st
import pydeck as pdk
import pydeck_carto as pdkc


@st.cache_resource
def fetch_data(bbox):
    gdf = fused.run("UDF_FEMA_Buildings_US", bbox=bbox)
    return gdf
gdf = fetch_data(bbox)

centroid_x = gdf.centroid.x.mean()
centroid_y = gdf.centroid.y.mean()

largest_area = gdf['SQMETERS'].max()

deck = st.empty()
categories = [
    "Assembly",
    "Commercial",
    "Utility and Misc",
    "Residential",
    "Industrial",
    "Education",
    "Government"
]
selected_category = st.selectbox("Choose a category:", ['All'] + categories)
if selected_category != 'All':
    gdf = gdf[gdf['OCC_CLS'] == selected_category]

percentage_slider = st.slider("Only keep the top percentile of building area:", 0, 100, 100)
area_threshold = percentage_slider * largest_area / 100

gdf = gdf[gdf["SQMETERS"] < area_threshold]

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

st.write(
    """
    This app was made by [Sina Kashuk](https://www.linkedin.com/in/skashuk/)
    """
)