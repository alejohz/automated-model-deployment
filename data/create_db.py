import gzip
import json
import os

import pandas as pd
import sqlalchemy
import wget
from dotenv import load_dotenv

load_dotenv()

DB_USER = "aeiwtyxk"
DB_NAME = "aeiwtyxk"
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = "rajje.db.elephantsql.com"
# This db is hosted in ElephantSql a free service for postgresql SQL DBs
# The password is hidden under the .env file


def get_connection():
    return sqlalchemy.create_engine(
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    )


engine = get_connection()  # create engine

# This dataset is extracted from the amazon reviews dataset
# This is only the gift cards category
url = "https://datarepo.eng.ucsd.edu/mcauley_group/data/amazon_v2/categoryFiles/Gift_Cards.json.gz"
filename = wget.download(url, out="data/")

### load the data
data = []
with gzip.open("Gift_Cards.json.gz") as f:
    for line in f:
        data.append(json.loads(line.strip()))


df = (
    pd.DataFrame.from_dict(data).dropna(  # read from dictionary
        subset=["reviewText", "asin", "reviewerID"]
    )
    # remove rows with empty reviewText
)[
    ["asin", "reviewerID", "reviewText"]
]  # select only id and text

# create the database
with engine.connect() as conn:
    df.to_sql("reviews", conn, schema="raw", if_exists="replace", index=False)
