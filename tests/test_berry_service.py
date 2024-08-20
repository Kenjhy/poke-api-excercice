import pytest
from app.services.berry_service import BerryService
from app.models.berry_stats_model import BerryStats
import time


@pytest.fixture
def berry_service():
    return BerryService()


def test_get_berry_stats(berry_service):
    # First call
    start_time = time.time()
    stats1 = berry_service.get_berry_stats()
    end_time = time.time()
    first_call_duration = end_time - start_time

    assert isinstance(stats1, BerryStats)
    assert len(stats1.berries_names) > 0
    assert stats1.min_growth_time <= stats1.max_growth_time
    assert stats1.variance_growth_time >= 0
    assert all(isinstance(freq, int) for freq in stats1.frequency_growth_time.values())

    # Second call (should be faster due to caching)
    start_time = time.time()
    stats2 = berry_service.get_berry_stats()
    end_time = time.time()
    second_call_duration = end_time - start_time

    # The second call should be significantly faster
    assert second_call_duration < first_call_duration

    # The results should be the same
    assert stats1 == stats2


def test_berry_stats_structure(berry_service):
    stats = berry_service.get_berry_stats()
    
    assert isinstance(stats.berries_names, list)
    assert isinstance(stats.min_growth_time, int)
    assert isinstance(stats.median_growth_time, float)
    assert isinstance(stats.max_growth_time, int)
    assert isinstance(stats.variance_growth_time, float)
    assert isinstance(stats.mean_growth_time, float)
    assert isinstance(stats.frequency_growth_time, dict)
    assert all(isinstance(k, int) and isinstance(v, int) for k, v in stats.frequency_growth_time.items())

    assert stats.min_growth_time <= stats.median_growth_time <= stats.max_growth_time
    assert stats.variance_growth_time >= 0
    assert sum(stats.frequency_growth_time.values()) == len(stats.berries_names)