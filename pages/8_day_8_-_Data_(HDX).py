import fused
import streamlit as st
import asyncio
from requests.models import PreparedRequest


async def install_micro_async():
    try:
        import micropip
        await micropip.install("geopandas")
        return 'w/ micro'
    except ImportError:
        return 'w/o micro'
# run_async_task(install_micro_async())
try:
    a = asyncio.run(install_micro_async())
except RuntimeError:
    print("Didn't run async")
    pass

import geopandas
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Fused 30 Days #8: Data (HDX)", page_icon="⚪️")
st.sidebar.header("Day 8 - Data (HDX)")
st.title("2021 Humanitarian Developlment Index per country")
st.markdown(
    """
    This is a map showing the 2021 Humanitarian Development Index from the [Human Development Data](https://data.humdata.org/dataset/human-development-data) dataset hosted on HDX.
    """
)

percentage_slider = st.slider("Highest percentage ranked of countries", 0, 100, 5)
st.write(f"Slider value: {percentage_slider=}")

m = folium.Map(location=[0, 0], zoom_start=2)
st_folium(m)


# Using HTTP request
# url_params = {"highest_percentage": percentage_slider}
# url_raster = "https://www.fused.io/server/v1/realtime-shared/fsh_49hXAtlrDDHr2MFvLBHlLW/run/file?dtype_out_vector=geojson"
# req = PreparedRequest()
# req.prepare_url(url_raster, url_params)
# st.write(f"{req.url=}")
# folium.GeoJson(req.url).add_to(m)

# Using fused.run()
# gdf = asyncio.Task(fused.run("fsh_49hXAtlrDDHr2MFvLBHlLW", highest_percentage=percentage_slider))
@st.cache_resource
def fetch_data(percent = percentage_slider):
    gdf = fused.run("fsh_49hXAtlrDDHr2MFvLBHlLW", highest_percentage=percent)
    # gdf = asyncio.Task(fused.run("fsh_49hXAtlrDDHr2MFvLBHlLW", highest_percentage=percent))
    return gdf


# out_data = fetch_data(percentage_slider)
# for k,v in out_data.items():
#     out = await v
    
#     gdf = out.data
#     st.write(f"Recieved gdf: {gdf.shape=}")
#     folium.GeoJson(gdf).add_to(m)
gdf = fetch_data(percentage_slider)
st.write(f"Recieved gdf: {gdf.shape=}")

folium.GeoJson(gdf).add_to(m)

