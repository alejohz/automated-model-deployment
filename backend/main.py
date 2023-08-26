import os

import pandas as pd
import sqlalchemy
from dotenv import load_dotenv
from fastapi import FastAPI
from textblob import TextBlob
from typing import List, Dict

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


app = FastAPI() # Create FastAPI instance

@app.get("/")
async def root() -> Dict:
    return {"message": "Hello World"}


@app.get("predict/{asin}")
def predict(asin: str) -> List[str]:
    connection = get_connection() # Get connection
    query = f"SELECT * FROM raw.reviews WHERE asin = '{asin}'" # SQL query
    # Read only first 5 for simplicity
    reviews = pd.read_sql(query, connection).reviewText.values[:5]
    if reviews.size == 0:
        return ["No reviews found"]
    sentiments = []
    for review in reviews:  # Iterate over reviews
        # Create a TextBlob object
        blob = TextBlob(review)
        # Perform sentiment analysis
        sentiment_score = blob.sentiment.polarity
        # Determine sentiment label
        if sentiment_score > 0:
            sentiment_label = "Positive"
        elif sentiment_score < 0:
            sentiment_label = "Negative"
        else:
            sentiment_label = "Neutral"
        sentiments.append(sentiment_label)
    return sentiments
