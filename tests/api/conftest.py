import pytest

import project
from themoviedb_tests.data.movies import fight_club
from themoviedb_tests.utils.api import tmdb_request, delete_all_rated_movies


@pytest.fixture(scope='function', autouse=False)
def clear_rated_movies():
    delete_all_rated_movies()
    yield
    delete_all_rated_movies()


@pytest.fixture(scope='function', autouse=False)
def fill_rated_movies():
    delete_all_rated_movies()
    tmdb_request('post', f'/movie/{fight_club.id}/rating',
                 json={'value': project.config.movie_rate_value})
