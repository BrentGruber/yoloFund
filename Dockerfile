FROM python:3.9

RUN pip install poetry

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/stock_tracker

WORKDIR /app
COPY . .

RUN poetry config virtualenvs.create false && poetry install
CMD poetry show && poetry run aerich upgrade && poetry run python stock_tracker/main.py