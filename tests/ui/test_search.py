from themoviedb_tests.pages.search_page import SearchPage


def test_search_page_contents():
    # ACT
    page = SearchPage()
    page.open()
    # ASSERT
    page.should_have_contents_visible()
