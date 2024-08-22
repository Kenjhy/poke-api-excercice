import pytest
from unittest.mock import patch, Mock
from app.repositories.berry_repository import BerryRepository
from app.models.berry_model import Berry


@pytest.fixture
def berry_repository():
    return BerryRepository()


@pytest.fixture(autouse=True)
def clear_cache(berry_repository):
    berry_repository.clear_cache()


@pytest.mark.usefixtures("clear_cache")
@patch('app.repositories.berry_repository.requests.get')
def test_get_all_berries(mock_get, berry_repository):
    # Mock the API responses
    mock_responses = [
        Mock(
            json=lambda: {
                'results': [{'url': 'https://pokeapi.co/api/v2/berry/1/'}],
                'next': None
            }
        ),
        Mock(
            json=lambda: {
                'name': 'cheri',
                'growth_time': 3
            }
        )
    ]
    mock_get.side_effect = mock_responses

    berries = berry_repository.get_all_berries()

    assert len(berries) == 1
    assert isinstance(berries[0], Berry)
    assert berries[0].name == 'cheri'
    assert berries[0].growth_time == 3

    # Check that the cache is working
    berry_repository.get_all_berries()
    assert mock_get.call_count == 2  # Should not increase due to caching


@pytest.mark.usefixtures("clear_cache")
@patch('app.repositories.berry_repository.requests.get')
def test_get_all_berries_pagination(mock_get, berry_repository):
    # Mock paginated API responses
    mock_responses = [
        Mock(
            json=lambda: {
                'results': [{'url': 'https://pokeapi.co/api/v2/berry/1/'}],
                'next': 'https://pokeapi.co/api/v2/berry?offset=20'
            }
        ),
        Mock(json=lambda: {'name': 'cheri', 'growth_time': 3}),
        Mock(
            json=lambda: {
                'results': [{'url': 'https://pokeapi.co/api/v2/berry/21/'}],
                'next': None
            }
        ),
        Mock(json=lambda: {'name': 'chesto', 'growth_time': 4})
    ]
    mock_get.side_effect = mock_responses

    berries = berry_repository.get_all_berries()

    print(f"Berries: {berries}")
    print(f"Mock call count: {mock_get.call_count}")
    print(f"Mock call args: {mock_get.call_args_list}")

    assert len(berries) == 2, f"Expected 2 berries, got {len(berries)}"
    assert berries[0].name == 'cheri', f"Expected first berry to be 'cheri', got {berries[0].name if berries else 'No berries'}"
    assert berries[1].name == 'chesto', f"Expected second berry to be 'chesto', got {berries[1].name if len(berries) > 1 else 'Not enough berries'}"
    assert mock_get.call_count == 4, f"Expected 4 API calls, got {mock_get.call_count}"

    # Verify that the mock was called with the correct URLs
    call_args_list = mock_get.call_args_list
    assert call_args_list[0][0][0] == berry_repository.base_url, f"First call should be to {berry_repository.base_url}, was {call_args_list[0][0][0]}"
    assert call_args_list[1][0][0] == 'https://pokeapi.co/api/v2/berry/1/', f"Second call should be to first berry URL, was {call_args_list[1][0][0]}"
    assert call_args_list[2][0][0] == 'https://pokeapi.co/api/v2/berry?offset=20', f"Third call should be to pagination URL, was {call_args_list[2][0][0]}"
    assert call_args_list[3][0][0] == 'https://pokeapi.co/api/v2/berry/21/', f"Fourth call should be to second berry URL, was {call_args_list[3][0][0]}"
    

@pytest.mark.usefixtures("clear_cache")
@patch('app.repositories.berry_repository.requests.get')
def test_get_all_berries_api_error(mock_get, berry_repository):
    mock_get.side_effect = Exception("API Error")

    with pytest.raises(Exception) as exc_info:
        berry_repository.get_all_berries()
    
    assert "API Error" in str(exc_info.value)


@pytest.mark.usefixtures("clear_cache")
@patch('app.repositories.berry_repository.requests.get')
def test_cache_expiration(mock_get, berry_repository):
    # First call setup
    mock_get.side_effect = [
        Mock(json=lambda: {'results': [{'url': 'https://pokeapi.co/api/v2/berry/1/'}], 'next': None}),
        Mock(json=lambda: {'name': 'cheri', 'growth_time': 3})
    ]

    # First call
    berry_repository.get_all_berries()
    initial_call_count = mock_get.call_count
    assert initial_call_count == 2  # One for the list, one for the berry details

    # Reset mock for second call
    mock_get.reset_mock()
    mock_get.side_effect = [
        Mock(json=lambda: {'results': [{'url': 'https://pokeapi.co/api/v2/berry/1/'}], 'next': None}),
        Mock(json=lambda: {'name': 'cheri', 'growth_time': 3})
    ]

    # Second call (should use cache)
    berry_repository.get_all_berries()
    assert mock_get.call_count == 0  # Should not make any calls due to cache

    # Simulate cache expiration
    berry_repository.clear_cache()

    # Reset mock for third call
    mock_get.reset_mock()
    mock_get.side_effect = [
        Mock(json=lambda: {'results': [{'url': 'https://pokeapi.co/api/v2/berry/1/'}], 'next': None}),
        Mock(json=lambda: {'name': 'cheri', 'growth_time': 3})
    ]

    # Third call (should make a new request)
    berry_repository.get_all_berries()
    assert mock_get.call_count == 2  # Should make calls again after cache cleared


if __name__ == "__main__":
    pytest.main()