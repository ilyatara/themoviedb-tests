from datetime import datetime

import pytest
import allure
from allure_commons.types import Severity

from themoviedb_tests.utils.file import get_path
from themoviedb_tests.utils.api import validate_schema, tmdb_request
from themoviedb_tests.data.movies import Movie


DEFAULT_PAGE_SIZE = 20


def assert_rating_descending(movies):
    previous_movie_rating = movies[0]['vote_average']
    for movie in movies[1:]:
        assert movie['vote_average'] <= previous_movie_rating
        premious_movie_rating = movie['vote_average']


@allure.tag('api')
@allure.severity(Severity.CRITICAL)
@allure.label('owner', 'Ilya Tarasov')
@allure.feature('Top rated movies')
@allure.title('Top rated movies are sorted by rating descending')
def test_get_top_rated_movies():
    # ACT
    response = tmdb_request('get', '/movie/top_rated')

    # ASSERT
    assert response.status_code == 200

    validate_schema(
        response.json(),
        get_path('tests', 'api', 'schemas', 'top_rated_movies.json')
    )

    movies = response.json()['results']
    assert len(movies) == DEFAULT_PAGE_SIZE

    assert_rating_descending(movies)


@allure.tag('api')
@allure.severity(Severity.CRITICAL)
@allure.label('owner', 'Ilya Tarasov')
@allure.feature('Top rated movies')
@allure.title('Top rated movies sorting with pagination')
@pytest.mark.parametrize('page_number', [2, 10, 50])
def test_top_rated_movies_pagination(page_number):
    # ARRANGE
    previous_page = tmdb_request('get', '/movie/top_rated', params={'page': page_number-1})

    # ACT
    current_page = tmdb_request('get', '/movie/top_rated', params={'page': page_number})

    # ASSERT
    assert current_page.status_code == 200

    validate_schema(
        current_page.json(),
        get_path('tests', 'api', 'schemas', 'top_rated_movies.json')
    )

    assert current_page.json()['results'][0]['vote_average'] <= \
           previous_page.json()['results'][-1]['vote_average']

    assert_rating_descending(current_page.json()['results'])


@allure.tag('api')
@allure.severity(Severity.CRITICAL)
@allure.label('owner', 'Ilya Tarasov')
@allure.feature('Top rated movies')
@allure.title('Movie data in the top rated list is correct')
@pytest.mark.parametrize('movie_index', range(0, 9, 19))
def test_data_in_top_rated_list_is_the_same_as_on_movie_details_page(movie_index):
    # ARRANGE
    response = tmdb_request('get', '/movie/top_rated')
    movie_from_list = response.json()['results'][movie_index]

    # ACT
    response = tmdb_request('get', f'/movie/{movie_from_list["id"]}')
    movie_details = response.json()

    # ASSERT
    for attribute in movie_from_list.keys():
        if movie_details.get(attribute):
            if attribute == 'vote_average':
                # on details page vote_average has 3 numbers after the decimal point
                assert movie_from_list[attribute] == round(movie_details[attribute], 1)
            elif attribute in ['vote_count', 'backdrop_path']:
                # these attributes' values may differ for some reason
                pass
            else:
                assert movie_from_list[attribute] == movie_details[attribute]
