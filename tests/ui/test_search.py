import allure
from allure_commons.types import Severity

from themoviedb_tests.pages.search_page import SearchPage
from themoviedb_tests.data.search_tabs import SearchTabs
from themoviedb_tests.data.movies import fight_club
from themoviedb_tests.data.people import justin


pytestmark = [
    allure.tag('web'),
    allure.severity(Severity.NORMAL),
    allure.label('owner', 'Ilya Tarasov'),
    allure.feature('Search'),
]


@allure.title('Contents of the search page are displayed correctly')
def test_search_page_contents():
    # ACT
    page = SearchPage()
    page.open()
    # ASSERT
    page.should_have_contents_visible()


@allure.title('Default text changes according to the active tab')
def test_select_search_tabs_with_no_results():
    # ARRANGE
    search_tabs_reversed = list([st for st in SearchTabs])[::-1]
    # ACT
    page = SearchPage()
    page.open()
    # ASSERT
    for st in search_tabs_reversed:
        page.should_have_search_tab_active_with_text(st)


@allure.title('Search suggestions are displayed on search input click')
def test_search_hints_are_visible_after_click_on_search_input():
    # ACT
    page = SearchPage()
    page.open()
    page.click_on_search_input()
    # ASSERT
    page.should_have_search_hints_visible()


@allure.title('Search suggestions are clickable')
def test_search_hints_are_functional():
    # ACT
    page = SearchPage()
    page.open()
    page.click_on_search_input()
    page.click_on_search_hint()
    # ASSERT
    page.should_have_movie_data_in_first_search_result()


@allure.title('Finding a movie by title')
def test_search_movie():
    # ACT
    page = SearchPage()
    page.open()
    page.send_search_query(fight_club.title)
    # ASSERT
    page.should_have_movie_data_in_first_search_result(
        fight_club.title,
        fight_club.release_date_in_ui_search_results,
        fight_club.overview,
        fight_club.id
    )


@allure.title('Finding a person by full name')
def test_search_person():
    # ACT
    page = SearchPage()
    page.open()
    page.send_search_query(justin.full_name)
    # ASSERT
    page.should_have_person_data_in_first_search_result(
        justin.full_name,
        justin.known_for,
        justin.movies,
        justin.id
    )
