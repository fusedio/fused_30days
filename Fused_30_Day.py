import streamlit as st

st.set_page_config(
    page_title="Fused 30 Days",
    page_icon="🌎",
)

st.title("Fused 30 Days App")

st.write("# Welcome to the Fused 30 Day Map Challenge page! 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    Fused is an end-to-end cloud platform for data analytics.
    You can build run Python function on our serverless platform, host them as individual apps or pooint to
    them through HTTP endpoints. 

    This page is a little demo of all the maps we & the community have built using Fused during the [2024 #30DayMapChallenge](https://30daymapchallenge.com/)


    ### Want to learn more?
    - Check out [our docs](https://docs.fused.io/)
    - Join [our waitlist](https://docs.google.com/forms/d/1NVzMjc2tXxlIgnFrxqQPM_NtG1B2AQ0En_pAbZHYSK0)
    - Join [the Discord](https://discord.com/invite/BxS5wMzdRk)
    - Follow us on [LinkedIn](https://www.linkedin.com/company/fusedio/) for more updates

"""
)