from themoviedb_tests.pages.search_page import SearchPage
from themoviedb_tests.data.search_tabs import SearchTabs


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
