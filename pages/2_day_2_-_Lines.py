# This is a streamlit app code
import numpy as np
import pandas as pd
import streamlit as st
import pydeck as pdk
import fused
import time

st.title("Day 2 - Lines")
st.write(
    """
    Here's a simple map with all the streets in SF!
    """
)

deck = st.empty()
view_state = pdk.ViewState(
    latitude=37.75,
    longitude=-122.40,
    zoom=14,
    pitch=0
)

@st.cache_data
def get_data(arg: int = 1):
    return fused.run("fsh_6N7iGIajMqacxK5fBJeW4k")

number_lines = st.slider('Number lines to load: ', 100, 15729, 100, 100)

gdf = get_data(1).sample(number_lines)

# Define the color style as a dictionary
style = {
    "tileLayer": {
        "type": "TileLayer",  # Note: removed @@ from @@type
        "minZoom": 0,
        "maxZoom": 19,
        "tileSize": 256,
        "pickable": True
    },
    "vectorLayer": {
        # "type": "GeoJsonLayer",  # Note: removed @@ from @@type
        "stroked": True,
        "filled": False,
        "pickable": True,
        "lineWidthMinPixels": 1,
        "pointRadiusMinPixels": 1,
        "getLineColor": [184, 184, 184],  # Default color, we'll handle color function separately
        "getFillColor": [208, 208, 208, 40]
    }
}


tile_layer = pdk.Layer(
    **style["tileLayer"]
)

geojson_layer = pdk.Layer(
    'GeoJsonLayer',
    gdf,
    get_line_color="get_color",
    **style["vectorLayer"],
)

def get_color(value):
    # Implementation for Tropic color scale
    # You can define your own color stops based on the domain [22, 8]
    if value is None:
        return [184, 184, 184]
    
    # Create a color scale mapping for the Tropic theme
    # These are example colors - adjust according to your needs
    colors = [
        [255, 87, 51],   # hot/high values
        [255, 166, 84],
        [255, 220, 138],
        [144, 238, 144], # middle values
        [0, 191, 191],
        [0, 127, 191],
        [0, 63, 191],    # cool/low values
    ]
    
    # Normalize the value between 0 and 1
    normalized = (value - 8) / (22 - 8)
    normalized = min(1, max(0, normalized))
    
    # Find the appropriate color
    idx = normalized * (len(colors) - 1)
    lower_idx = int(np.floor(idx))
    upper_idx = min(lower_idx + 1, len(colors) - 1)
    fraction = idx - lower_idx
    
    # Interpolate between colors
    color = [
        int(colors[lower_idx][i] * (1 - fraction) + colors[upper_idx][i] * fraction)
        for i in range(3)
    ]
    
    return color

updated_deck = pdk.Deck(
    layers=[
        tile_layer, 
        geojson_layer
        ],
    initial_view_state=view_state,
    map_style='mapbox://styles/mapbox/light-v9'
)

# Display the updated map in Streamlit
deck.pydeck_chart(updated_deck)


st.write(
    """
    This app was made by [Isaac Brodsky](https://www.linkedin.com/in/isaacbrodsky/)
    """
)