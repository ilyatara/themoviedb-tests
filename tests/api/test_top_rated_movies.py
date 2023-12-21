import pytest
import allure
from allure_commons.types import Severity

from themoviedb_tests.utils.file import get_abs_path
from themoviedb_tests.utils.api import validate_schema, tmdb_request


pytestmark = [
    allure.tag('api'),
    allure.severity(Severity.CRITICAL),
    allure.label('owner', 'Ilya Tarasov'),
    allure.feature('Top rated movies')
]


DEFAULT_PAGE_SIZE = 20
# TOP_RATED_MOVIES_URL = '/movie/top_rated'      # deprecated
VOTE_COUNT = 1000
TOP_RATED_MOVIES_URL = f'/discover/movie?sort_by=vote_average.desc&vote_count.gte={VOTE_COUNT}'


def assert_rating_descending(movies):
    previous_movie_rating = movies[0]['vote_average']
    for movie in movies[1:]:
        assert movie['vote_count'] >= VOTE_COUNT
        assert movie['vote_average'] <= previous_movie_rating
        previous_movie_rating = movie['vote_average']


@allure.title('Top rated movies are sorted by rating descending')
def test_get_top_rated_movies():
    # ACT
    response = tmdb_request('get', TOP_RATED_MOVIES_URL)
    # ASSERT
    assert response.status_code == 200
    validate_schema(
        response.json(),
        get_abs_path('tests/api/schemas/top_rated_movies.json')
    )
    movies = response.json()['results']
    assert len(movies) == DEFAULT_PAGE_SIZE
    assert_rating_descending(movies)


@allure.title('Top rated movies sorting with pagination')
@pytest.mark.parametrize('page_number', [2, 10, 50])
def test_top_rated_movies_pagination(page_number):
    # ARRANGE
    previous_page_resp = tmdb_request('get', TOP_RATED_MOVIES_URL, params={'page': page_number-1})
    # ACT
    current_page_resp = tmdb_request('get', TOP_RATED_MOVIES_URL, params={'page': page_number})
    # ASSERT
    assert current_page_resp.status_code == 200
    validate_schema(
        current_page_resp.json(),
        get_abs_path('tests/api/schemas/top_rated_movies.json')
    )
    previous_page = previous_page_resp.json()['results']
    current_page = current_page_resp.json()['results']
    assert previous_page[-1]['vote_average'] >= current_page[0]['vote_average']
    assert_rating_descending(current_page)


@allure.title('Movie data in the top rated list is correct')
@pytest.mark.parametrize('movie_index', range(20))
def test_data_in_top_rated_list_is_the_same_as_on_movie_details_page(movie_index):
    # ARRANGE
    response = tmdb_request('get', TOP_RATED_MOVIES_URL)
    movie_from_list = response.json()['results'][movie_index]
    # ACT
    response = tmdb_request('get', f'/movie/{movie_from_list["id"]}')
    movie_details = response.json()
    # ASSERT
    for attribute in movie_from_list.keys():
        if movie_details.get(attribute):
            if attribute in ['vote_count', 'backdrop_path']:
                # these attributes' values may differ for some reason
                pass
            elif attribute == 'vote_average':
                # vote_average on the details page is rounded to 1 digit after the decimal point
                assert movie_from_list['vote_average'] == round(movie_details['vote_average'], 1)
            else:
                assert movie_from_list[attribute] == movie_details[attribute]
