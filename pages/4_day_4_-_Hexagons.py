import streamlit as st
import pydeck as pdk
import fused

st.sidebar.header("Day 4 - Hexagons")

st.title("🖼️ Hexify any image!")

st.markdown("""
Paste a URL to your favorite `.png` image below and see it get processed to H3.

This app calls the ["Hexify Image"](https://www.fused.io/workbench/catalog/Hexify_Image-b817f7fd-cd52-40d3-a601-d0fcc36d0f86) UDF by [Jennings Anderson](https://www.linkedin.com/in/jenningsanderson/). The H3 resolution and URL of your image are passed as input parameters to the UDF.
""")

h3_res = st.selectbox("H3 resolution", [5,6,7,8,9])

image_url = st.text_input('URL of image to Hexify:', value="https://fused-magic.s3.us-west-2.amazonaws.com/thumbnails/udfs-staging/jennings.png")

df = fused.run('UDF_Hexify_Image', path=image_url, res=h3_res)
df['hex'] = df['hex'].apply(lambda x: hex(x)[2:].lower())

# Define a layer to display on a map
layer = pdk.Layer(
    "H3HexagonLayer",
    df,
    pickable=True,
    stroked=True,
    filled=True,
    extruded=True,
    get_hexagon="hex",
    get_fill_color="[value, value, value]",
    get_line_color=[25, 25, 255],
    line_width_min_pixels=2,
    get_elevation='value^2',
    elevation_scale=50
)

# Set the viewport location

view_state = pdk.ViewState(latitude=0.4, longitude=0.5, zoom=8, bearing=10, pitch=10)


# Render
r = pdk.Deck(layers=[layer], initial_view_state=view_state)
event = st.pydeck_chart(r)
