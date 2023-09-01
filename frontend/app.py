import streamlit as st
import plotly.express as px
import requests

from utils.utils import app_base_config, load_css, get_product_names

app_base_config()
load_css("assets/style.css")

st.write("# Welcome to the Sentiment prediction ML demo! 👋")

df = get_product_names()
summary = st.selectbox("Select a product", df.summary.tolist())

if st.button("Predict"):
    asin = df[df.summary == summary].asin.values[0]
    response = requests.get(
        f"https://unexpected-second-stomach.glitch.me/predict/{asin}"
    )
    fig = px.bar(
        response.json(),
        title="Distribution of reviews",
        y_title="Count",
        x_title="Sentiment",
    )

    st.plotly_chart(fig, use_container_width=True)
