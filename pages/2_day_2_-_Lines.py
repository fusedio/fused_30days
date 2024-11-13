import numpy as np
import streamlit as st
import pydeck as pdk
import fused

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

style = {
    "tileLayer": {
        "type": "TileLayer",
        "minZoom": 0,
        "maxZoom": 19,
        "tileSize": 256,
        "pickable": True
    },
    "vectorLayer": {
        "stroked": True,
        "filled": False,
        "pickable": True,
        "lineWidthMinPixels": 3,
        "pointRadiusMinPixels": 1,
        "getLineColor": [22, 22, 22],
        "getFillColor": [208, 208, 208, 40]
    }
}


tile_layer = pdk.Layer(
    **style["tileLayer"]
)

geojson_layer = pdk.Layer(
    'GeoJsonLayer',
    gdf,
    **style["vectorLayer"],
)


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