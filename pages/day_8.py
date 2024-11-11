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
st.write(a)
import geopandas
st.write('Done')