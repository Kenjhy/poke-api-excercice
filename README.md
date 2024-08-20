# Poke-berries Statistics API

This project provides a FastAPI-based API for Poke-berries statistics.

## Setup

1. Install dependencies:
   ```
   poetry install
   ```

2. Set up environment variables in `.env` file.

## Running the Application

```
poetry run uvicorn app.main:app --reload
```

## Running Tests

```
poetry run pytest
```

## Deployment

This application can be deployed to Pythonanywhere or a similar cloud service.

For Pythonanywhere:

## API Endpoints

- `/allBerryStats`: Get statistics on all berries
- `/berryStatsHistogram`: Get a histogram of berry growth times
- `/apiInfo`: Get API configuration information