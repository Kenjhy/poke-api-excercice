import requests
from app.models.berry_model import Berry
from typing import List
from cachetools import cached, TTLCache
import os
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class BerryRepository:
    def __init__(self):
        self.base_url = f"{os.getenv('POKEAPI_BASE_URL', 'https://pokeapi.co/api/v2')}{os.getenv('BERRY_ENDPOINT', '/berry')}"
        self.cache = TTLCache(
            maxsize=int(os.getenv('CACHE_MAXSIZE', '1')),
            ttl=int(os.getenv('CACHE_TTL', '3600'))
        )

    @cached(cache=TTLCache(maxsize=1, ttl=3600))
    def get_all_berries(self) -> List[Berry]:
        berries = []
        next_url = self.base_url
        logger.debug(f"Starting to fetch berries from {next_url}")

        while next_url:
            logger.debug(f"Fetching from {next_url}")
            response = requests.get(next_url)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"Received data: {data}")
            
            if 'results' in data:
                for item in data['results']:
                    logger.debug(f"Fetching berry details from {item['url']}")
                    berry_data = requests.get(item['url']).json()
                    logger.debug(f"Berry data: {berry_data}")
                    if 'name' in berry_data and 'growth_time' in berry_data:
                        berry = Berry(name=berry_data['name'], growth_time=berry_data['growth_time'])
                        berries.append(berry)
                        logger.debug(f"Added berry: {berry}")
            
            next_url = data.get('next')
            logger.debug(f"Next URL: {next_url}")

        logger.debug(f"Total berries fetched: {len(berries)}")
        return berries

    def clear_cache(self):
        self.get_all_berries.cache_clear()
        logger.debug("Cache cleared")