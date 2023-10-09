import pytest

import project
from themoviedb_tests.utils.api import tmdb_request
from themoviedb_tests.data.movies import fight_club


def clear_rated_movies():
    response = tmdb_request('get', f'/account/{project.config.tmdb_account_id}/rated/movies')
    rated_movies_ids = [movie['id'] for movie in response.json()['results']]
    for movie_id in rated_movies_ids:
        tmdb_request('delete', f'/movie/{movie_id}/rating')


@pytest.fixture(scope='function', autouse=False)
def clear_rated_movies_list():
    clear_rated_movies()
    yield
    clear_rated_movies()


@pytest.fixture(scope='function', autouse=False)
def fill_rated_movies_list():
    clear_rated_movies()
    tmdb_request('post', f'/movie/{fight_club.id}/rating',
                 json={'value': project.config.movie_rate_value})
    yield
