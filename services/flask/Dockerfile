FROM python:3.10.7-slim-buster
LABEL authors="Zuice"

WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip installl --no-cache -r requirements.txt

COPY . /app

EXPOSE 5000