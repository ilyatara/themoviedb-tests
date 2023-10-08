from themoviedb_tests.pages.search_page import SearchPage
from themoviedb_tests.data.search_tabs import SearchTabs
from themoviedb_tests.data.movies import fight_club
from themoviedb_tests.data.people import justin


def test_search_page_contents():
    # ACT
    page = SearchPage()
    page.open()
    # ASSERT
    page.should_have_contents_visible()


def test_select_search_tabs_with_no_results():
    # ARRANGE
    search_tabs_reversed = list([st for st in SearchTabs])[::-1]
    # ACT
    page = SearchPage()
    page.open()
    # ASSERT
    for st in search_tabs_reversed:
        page.should_have_search_tab_active_with_text(st)


def test_search_hints_are_visible_after_click_on_search_input():
    # ACT
    page = SearchPage()
    page.open()
    page.click_on_search_input()
    # ASSERT
    page.should_have_search_hints_visible()


def test_search_hins_are_functional():
    # ACT
    page = SearchPage()
    page.open()
    page.click_on_search_input()
    page.click_on_search_hint()
    # ASSERT
    page.should_have_movie_data_in_first_search_result()


def test_search_movie():
    # ACT
    page = SearchPage()
    page.open()
    page.send_search_request(fight_club.title)
    # ASSERT
    page.should_have_movie_data_in_first_search_result(
        fight_club.title,
        fight_club.release_date_in_ui_search_results,
        fight_club.overview,
        fight_club.id
    )

def test_search_person():
    # ACT
    page = SearchPage()
    page.open()
    page.send_search_request(justin.full_name)
    # ASSERT
    page.should_have_person_data_in_first_search_result(
        justin.full_name,
        justin.known_for,
        justin.movies,
        justin.id
    )
