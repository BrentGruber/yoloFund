FROM python:3.9

RUN pip3 install poetry

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/stock_tracker

WORKDIR /app
COPY . .

RUN poetry config virtualenvs.create false
RUN poetry install
CMD poetry install && poetry run aerich upgrade && poetry run python stock_tracker/main.py