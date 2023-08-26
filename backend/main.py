import os

import pandas as pd
import sqlalchemy
from dotenv import load_dotenv
from fastapi import FastAPI
from textblob import TextBlob

load_dotenv()

# This app was deployed in glitch
# Url: https://roomy-angry-trapezoid.glitch.me/
DB_USER = "aeiwtyxk"
DB_NAME = "aeiwtyxk"
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = "rajje.db.elephantsql.com"


def get_connection() -> sqlalchemy.engine.base.Connection:
    return sqlalchemy.create_engine(
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    )


app = FastAPI() # Create FastAPI instance

@app.get("/")
async def root() -> dict:
    return {"message": "Hello World"}


@app.get("predict/{asin}")
def predict(asin: str) -> str:
    connection = get_connection() # Get connection
    query = f"SELECT * FROM reviews WHERE asin = '{asin}'" # SQL query
    # Create a TextBlob object
    blob = TextBlob(pd.read_sql(query, connection).reviewText.values[0])

    # Perform sentiment analysis
    sentiment_score = blob.sentiment.polarity

    # Determine sentiment label
    if sentiment_score > 0:
        sentiment_label = "Positive"
    elif sentiment_score < 0:
        sentiment_label = "Negative"
    else:
        sentiment_label = "Neutral"
    return sentiment_label
