import statistics
from typing import List
from functools import lru_cache
from app.models.berry_stats_model import BerryStats
from app.repositories.berry_repository import BerryRepository


class BerryService:
    def __init__(self):
        self.repository = BerryRepository()

    @lru_cache(maxsize=1)
    def get_berry_stats(self) -> BerryStats:
        berries = self.repository.get_all_berries()
        if not berries:
            raise ValueError("No berries found")

        growth_times = [berry.growth_time for berry in berries]

        return BerryStats(
            berries_names=[berry.name for berry in berries],
            min_growth_time=min(growth_times),
            median_growth_time=statistics.median(growth_times),
            max_growth_time=max(growth_times),
            variance_growth_time=self._calculate_variance(growth_times),
            mean_growth_time=statistics.mean(growth_times),
            frequency_growth_time=self._calculate_frequency(growth_times)
        )

    def _calculate_variance(self, growth_times: List[int]) -> float:
        if len(growth_times) < 2:
            return 0.0
        mean = sum(growth_times) / len(growth_times)
        return sum((x - mean) ** 2 for x in growth_times) / (len(growth_times) - 1)

    def _calculate_frequency(self, growth_times: List[int]) -> dict:
        return {time: growth_times.count(time) for time in set(growth_times)}

    def clear_cache(self):
        self.get_berry_stats.cache_clear()