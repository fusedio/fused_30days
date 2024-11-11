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

st.write(a)
import geopandas
st.write('Done')