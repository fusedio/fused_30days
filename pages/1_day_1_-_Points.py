import pydeck as pdk
import streamlit as st
import geopandas as gpd

st.title("Day1 - Point(s)")
st.sidebar.header("Day 1 - Points")

st.write(
    """
    Here's a simple point, on a map
    Doesn't get much simpler than that does it?

    You can change the buffer side around it 👇
    Or take a look at the code for yourself on the side 👈
    """
)

center_point = [-122.40, 37.75]

deck = st.empty()
view_state = pdk.ViewState(
    latitude=center_point[1],
    longitude=center_point[0],
    zoom=11,
    pitch=0
)
initial_deck = pdk.Deck(
    initial_view_state=view_state,
    map_style='mapbox://styles/mapbox/light-v9'
)

radius_km = st.slider('Buffer radius (1/100th degree)', 0.1, 100.0, 1.0, 0.1)

# Initiate geojson
point_geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Point",
                "coordinates": center_point
            }
        }
    ]
}

point_gdf = gpd.GeoDataFrame.from_features(point_geojson['features'], crs='EPSG:3857')

buffer = point_gdf.copy()
buffer.geometry = point_gdf.geometry.buffer(radius_km/100)


buffer_layer = pdk.Layer(
    'GeoJsonLayer',
    buffer,
    opacity=0.5,
    stroked=True,
    filled=True,
    extruded=False,
    wire_frame=True,
    get_fill_color=[255, 165, 0],  # Orange fill
    get_line_color=[255, 140, 0],  # Darker orange outline
    get_line_width=2,
)

point_layer = pdk.Layer(
    'GeoJsonLayer',
    point_geojson,
    opacity=1,
    get_point_radius=10,
    get_fill_color=[255, 0, 0],  # Red point
    pointer_events=True
)



updated_layer = pdk.Deck(
    layers=[buffer_layer, point_layer],
    initial_view_state=view_state,
    map_style='mapbox://styles/mapbox/light-v9'
)
st.pydeck_chart(updated_layer)