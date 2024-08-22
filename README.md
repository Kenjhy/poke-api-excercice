# PokeAPI Berry Statistics API

This project provides an API for retrieving statistics about berries from the PokeAPI. It is built using Python, FastAPI, and various other libraries.

## Project Structure

The project follows the following directory structure:

```
poke-api-excercise/
├── .elasticbeanstalk/
│   └── config.yml
├── app/
│   ├── controllers/
│   │   └── berry_controller.py
│   ├── models/
│   │   ├── berry_model.py
│   │   └── berry_stats_model.py
│   ├── repositories/
│   │   └── berry_repository.py
│   ├── services/
│   │   └── berry_service.py
│   ├── templates/
│   │   └── histogram_template.html
│   ├── utils/
│   │   └── histogram.py
│   ├── main.py
├── ebextensions/
│   ├── 01_fastapi.config
│   ├── 02_env.config
│   └── 02_env.config  
├── tests/
│   ├── test_berry_repository.py
│   └── test_berry_service.py
├── .env
├── .gitignore
├── Dockerfile  
├── Procfile
├── pyproject.toml
├── README.md
└── requirements.txt
```

## Technologies Used

- Python 3.10
- FastAPI 0.112.1
- Pydantic 2.8.2
- Requests 2.32.3
- Pytest 8.3.2
- Matplotlib 3.9.2
- Docker
- AWS Elastic Beanstalk

## Setup

### Prerequisites

- Python 3.10 installed
- Poetry installed (for dependency management)
- Docker installed (optional, for running in a container)
- An external API is consumed from the following documentation: https://pokeapi.co/docs/v2#berries

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/Kenjhy/poke-api-excercice.git
   cd poke-api-excercise
   ```

2. Install the dependencies using Poetry:
   ```
   poetry install
   ```

### Configuration

The application uses environment variables for configuration. You can set the environment variables in a `.env` file. Here's an example `.env` file:

```
API_HOST=0.0.0.0
API_PORT=8000
POKEAPI_BASE_URL=https://pokeapi.co/api/v2
BERRY_ENDPOINT=/berry
CACHE_TTL=3600
CACHE_MAXSIZE=1
```

## Running the Application

### Using Poetry

To run the application using Poetry, use the following command:

```
poetry run uvicorn app.main:app --reload
```

The API will be accessible at `http://localhost:8000`.

### Using Docker

To run the application using Docker, follow these steps:

1. Build the Docker image:
   ```
   docker build -t poke-berries-api .
   ```

2. Run the Docker container:
   ```
   docker run --env-file .env -p 8000:8000 poke-berries-api
   ```

The API will be accessible at `http://localhost:8000`.

## API Endpoints

The following endpoints are available:

- `GET /allBerryStats`: Retrieves statistics about all berries.
- `GET /berryStatsHistogram`: Displays a histogram of berry growth times.
- `GET /apiInfo`: Provides information about the API configuration.

## Testing

To run the tests, use the following command:

```
poetry run pytest
```

## Deployment

The application was deployed on AWS Elastic Beanstalk. The following steps were used:

1. Create an Elastic Beanstalk environment.

2. Configure the environment with the necessary settings.

3. Deploy the application using the `eb deploy` command.

The deployed API can be accessed at:
- http://poke-api-excercise-env.eba-e6fcpx4e.us-east-1.elasticbeanstalk.com/allBerryStats
- http://poke-api-excercise-env.eba-e6fcpx4e.us-east-1.elasticbeanstalk.com/berryStatsHistogram  
- http://poke-api-excercise-env.eba-e6fcpx4e.us-east-1.elasticbeanstalk.com/apiInfo

## Caching

The application uses caching to speed up the API queries. The caching is implemented using the `cachetools` library. The cache size and time-to-live (TTL) can be configured using the `CACHE_MAXSIZE` and `CACHE_TTL` environment variables, respectively.

## Histogram

The application uses the Matplotlib library to generate a histogram of berry growth times. The histogram is displayed on an HTML page when accessing the `/berryStatsHistogram` endpoint.

## Models

The application uses Pydantic for data modeling and validation. Pydantic ensures that the data passed around in the application adheres to the defined schemas. The following models are used:

The `Berry` model represents a berry

he `BerryStats` model represents the statistics of berries

These models are defined in the `app/models` directory.