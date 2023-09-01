import os

import pandas as pd
import sqlalchemy
from dotenv import load_dotenv
import streamlit as st


def app_base_config():
    st.set_page_config(
        page_title="Sentiment Prediction",
        initial_sidebar_state="expanded",
        layout="wide",
        page_icon="frontend/assets/favicon.png",
    )


def load_css(file_name: str) -> None:
    """Import a CSS file into the Streamlit app."""
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_dotenv()

# This app was deployed in glitch
# Url: https://unexpected-second-stomach.glitch.me/
DB_USER = "aeiwtyxk"
DB_NAME = "aeiwtyxk"
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = "rajje.db.elephantsql.com"


def get_connection() -> sqlalchemy.engine.base.Connection:
    return sqlalchemy.create_engine(
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    )

def get_product_names() -> pd.DataFrame:
    connection = get_connection() # Get connection
    query = f"SELECT * FROM raw.reviews LIMIT 5" # SQL query
    # Read only first 5 for simplicity
    reviews = pd.read_sql(query, connection)
    return reviews # Return unique product names
