import pytest
from unittest.mock import Mock
from app.services.berry_service import BerryService
from app.models.berry_stats_model import BerryStats
from app.models.berry_model import Berry


@pytest.fixture
def mock_repository():
    return Mock()


@pytest.fixture
def berry_service(mock_repository):
    service = BerryService()
    service.repository = mock_repository
    yield service
    service.clear_cache()  # Clear cache after each test


def test_get_berry_stats(berry_service, mock_repository):
    mock_berries = [
        Berry(name="cheri", growth_time=3),
        Berry(name="chesto", growth_time=3),
        Berry(name="pecha", growth_time=3),
        Berry(name="rawst", growth_time=3),
        Berry(name="aspear", growth_time=3),
    ]
    mock_repository.get_all_berries.return_value = mock_berries

    stats1 = berry_service.get_berry_stats()
    stats2 = berry_service.get_berry_stats()

    assert isinstance(stats1, BerryStats)
    assert len(stats1.berries_names) == 5
    assert stats1.min_growth_time == 3
    assert stats1.max_growth_time == 3
    assert stats1.median_growth_time == 3
    assert stats1.variance_growth_time == 0
    assert stats1.mean_growth_time == 3
    assert stats1.frequency_growth_time == {3: 5}

    assert stats1 == stats2
    mock_repository.get_all_berries.assert_called_once()


@pytest.mark.parametrize("berries,expected", [
    (
        [Berry(name="test", growth_time=5)],
        BerryStats(
            berries_names=["test"],
            min_growth_time=5,
            median_growth_time=5.0,
            max_growth_time=5,
            variance_growth_time=0.0,
            mean_growth_time=5.0,
            frequency_growth_time={5: 1}
        )
    ),
    (
        [Berry(name="test1", growth_time=3), Berry(name="test2", growth_time=7)],
        BerryStats(
            berries_names=["test1", "test2"],
            min_growth_time=3,
            median_growth_time=5.0,
            max_growth_time=7,
            variance_growth_time=8.0,
            mean_growth_time=5.0,
            frequency_growth_time={3: 1, 7: 1}
        )
    ),
])
def test_get_berry_stats_calculations(berry_service, mock_repository, berries, expected):
    mock_repository.get_all_berries.return_value = berries
    result = berry_service.get_berry_stats()
    assert result.berries_names == expected.berries_names
    assert result.min_growth_time == expected.min_growth_time
    assert result.max_growth_time == expected.max_growth_time
    assert result.median_growth_time == pytest.approx(expected.median_growth_time)
    assert result.variance_growth_time == pytest.approx(expected.variance_growth_time)
    assert result.mean_growth_time == pytest.approx(expected.mean_growth_time)
    assert result.frequency_growth_time == expected.frequency_growth_time


def test_empty_berry_list(berry_service, mock_repository):
    mock_repository.get_all_berries.return_value = []
    with pytest.raises(ValueError, match="No berries found"):
        berry_service.get_berry_stats()


@pytest.fixture(autouse=True)
def set_env_vars(monkeypatch):
    monkeypatch.setenv("CACHE_MAXSIZE", "1")
    monkeypatch.setenv("CACHE_TTL", "3600")