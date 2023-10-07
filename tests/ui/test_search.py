from themoviedb_tests.pages.search_page import SearchPage
from themoviedb_tests.data.search_tabs import SearchTabs
from themoviedb_tests.data.movies import fight_club


def test_search_page_contents():
    # ACT
    page = SearchPage()
    page.open()
    # ASSERT
    page.should_have_contents_visible()


def test_select_search_tabs_with_no_results():
    # ACT
    page = SearchPage()
    page.open()
    # ASSERT
    search_tabs_reversed = list([st for st in SearchTabs])[::-1]
    for st in search_tabs_reversed:
        page.should_have_search_tab_active_with_text(st)


def test_search_hints_are_visible_after_click_on_search_input():
    page = SearchPage()
    page.open()
    page.click_on_search_input()
    page.should_have_search_hints_visible()


def test_search_hins_are_functional():
    page = SearchPage()
    page.open()
    page.click_on_search_input()
    page.click_on_search_hint()
    page.first_search_result_should_have_movie_data()


def test_search_movie():
    page = SearchPage()
    page.open()
    page.send_search_request(fight_club.title)
    page.first_search_result_should_have_movie_data(
        fight_club.title,
        fight_club.release_date_in_ui_search_results,
        fight_club.overview
    )
