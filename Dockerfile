FROM python:3.9

RUN pip install poetry

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/stock_tracker

WORKDIR /app
COPY . .

RUN poetry install
CMD poetry run aerich upgrade && poetry run python stock_tracker/main.py