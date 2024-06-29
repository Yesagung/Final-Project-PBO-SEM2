FROM python:3.10 AS build

COPY app /app
COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app
RUN chmod +x run.sh

