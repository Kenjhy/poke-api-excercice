FROM python:3.10

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

COPY . .

# Establece las variables de entorno predeterminadas
ENV API_HOST=0.0.0.0
ENV API_PORT=8000
ENV POKEAPI_BASE_URL=https://pokeapi.co/api/v2
ENV BERRY_ENDPOINT=/berry
ENV CACHE_TTL=3600
ENV CACHE_MAXSIZE=1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]