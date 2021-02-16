# YoloFund

Yolofund is an application that will be able to scrape multiple sources to find popular stock tickers.  It will be able to count the number of times a particular ticker has been mentioned and analyze how that stock performs relative to the number of mentions in different sources such as reddit or twitter.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

You can either run the project using docker-compose or directly with poetry.

* In both cases you will need to create a .env file in the root directory with integration info. You can find an example in .env-example

Docker-Compose:

```
docker-compose up
```

Poetry:

```
poetry run python stock_tracker/main.py
```