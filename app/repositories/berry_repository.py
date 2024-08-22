import requests
from app.models.berry_model import Berry
from typing import List
from cachetools import cached, TTLCache
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BerryRepository:
    def __init__(self):
        logger.info(f"CACHE_MAXSIZE: {os.getenv('CACHE_MAXSIZE')}")
        logger.info(f"CACHE_TTL: {os.getenv('CACHE_TTL')}")
        self.base_url = f"{os.getenv('POKEAPI_BASE_URL', 'https://pokeapi.co/api/v2')}{os.getenv('BERRY_ENDPOINT', '/berry')}"
        self.cache = TTLCache(
            maxsize=int(os.getenv('CACHE_MAXSIZE', '1')),
            ttl=int(os.getenv('CACHE_TTL', '3600'))
        )

    @cached(cache=TTLCache(maxsize=int(os.getenv('CACHE_MAXSIZE', '1')), ttl=int(os.getenv('CACHE_TTL', '3600'))))
    def get_all_berries(self) -> List[Berry]:
        berries = []
        next_url = self.base_url

        while next_url:
            try:
                response = requests.get(next_url)
                response.raise_for_status()
            except requests.RequestException as e:
                raise Exception(f"Error getting data from PokeAPI: {e}")

            data = response.json()
            
            for item in data['results']:
                berry_data = requests.get(item['url']).json()
                berries.append(Berry(name=berry_data['name'], growth_time=berry_data['growth_time']))
            
            next_url = data.get('next')

        return berries