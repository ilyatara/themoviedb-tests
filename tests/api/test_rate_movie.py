import time

import project
from themoviedb_tests.utils.file import get_path
from themoviedb_tests.utils.api import validate_schema, tmdb_request
from themoviedb_tests.data.movies import fight_club


def test_get_rated_movies_list(fill_rated_movies_list):
    # ACT
    time.sleep(project.config.api_timeout)  # wait after request in fixture for the list to get updated
    response = tmdb_request('get', f'/account/{project.config.tmdb_account_id}/rated/movies')
    # ASSERT
    assert response.status_code == 200
    validate_schema(response.json(), get_path('tests', 'api', 'schemas', 'rated_movies.json'))
    movie_from_response = response.json()['results'][0]
    assert movie_from_response['title'] == fight_club.title
    assert movie_from_response['id'] == fight_club.id
    assert movie_from_response['original_language'] == fight_club.original_language
    assert movie_from_response['release_date'] == fight_club.release_date
    assert movie_from_response['rating'] == project.config.movie_rate_value


def test_add_movie_rate(clear_rated_movies_list):
    # ACT
    response = tmdb_request('post', f'/movie/{fight_club.id}/rating',
                            json={'value': project.config.movie_rate_value})
    # ASSERT
    assert response.status_code == 201
    assert list(response.json().keys()) == ['success', 'status_code', 'status_message']
    time.sleep(project.config.api_timeout)
    rated_movies = tmdb_request('get', f'/account/{project.config.tmdb_account_id}/rated/movies')
    assert len(rated_movies.json()['results']) == 1
    assert rated_movies.json()['results'][0]['title'] == fight_club.title
    assert rated_movies.json()['results'][0]['rating'] == project.config.movie_rate_value


def test_delete_movie_rate(fill_rated_movies_list):
    # ACT
    response = tmdb_request('delete', f'/movie/{fight_club.id}/rating')
    # ASSERT
    assert response.status_code == 200
    assert list(response.json().keys()) == ['success', 'status_code', 'status_message']
    time.sleep(project.config.api_timeout)
    rated_movies = tmdb_request('get', f'/account/{project.config.tmdb_account_id}/rated/movies')
    assert rated_movies.json()['results'] == []
