import streamlit as st
import asyncio
async def install_micro_async():
    try:
        import micropip
        await micropip.install("geopandas")
        return 'w/ micro'
    except ImportError:
        return 'w/o micro'
a = asyncio.run(install_micro_async())

st.set_page_config(page_title="Fused 30 Days #8: Data (HDX)", page_icon="⚪️")
st.sidebar.header("Day 8 - Data (HDX)")

import geopandas

st.title("2021 Humanitarian Developlment Index per country")

st.markdown(
    """
    This is a map showing the 2021 Humanitarian Development Index from the [Human Development Data](https://data.humdata.org/dataset/human-development-data) dataset hosted on HDX.
    """
)


import folium
from streamlit_folium import st_folium


m = folium.Map(location=[0, 0], zoom_start=2)

url_raster = "https://www.fused.io/server/v1/realtime-shared/fsh_49hXAtlrDDHr2MFvLBHlLW/run/file?dtype_out_raster=png&dtype_out_vector=geojson"

folium.GeoJson(url_raster).add_to(m)
st_folium(m)

