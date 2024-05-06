FROM python:3.12-slim

WORKDIR /app


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  && apt -y install curl \
  libpq-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .