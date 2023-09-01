FROM python:3.10-buster

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . app/
WORKDIR /app

ARG DB_PASSWORD
ENV DB_PASSWORD ${DB_PASSWORD}


CMD uvicorn main:app