from selene import browser, be, have

from themoviedb_tests import utils
from themoviedb_tests.data.search_tabs import SearchTabs


class SearchPage:
    url = '/search'
    search_input = browser.element('#search_v4')
    search_menu = browser.element('.grey_column')
    search_menu_tabs_ids = ', '.join([st.css_id for st in SearchTabs])
    search_menu_tabs = browser.all(search_menu_tabs_ids)
    search_menu_tabs_count = len(SearchTabs)
    search_menu_tabs_counters = browser.all('#search_menu_scroller span')
    search_results_container = browser.element('.white_column')

    def open(self):
        browser.open(self.url)
        utils.ui.close_cookies_banner()

    def should_have_contents_visible(self):
        # TODO: check that search suggestions are not available
        self.search_input.should(be.visible)
        self.search_menu.should(be.visible)
        self.search_results_container.should(be.visible)
        self.search_menu_tabs.should(
            have.size(self.search_menu_tabs_count)
        )
        self.search_menu_tabs_counters.should(
            have.exact_texts(['0'] * self.search_menu_tabs_count)
        )
        # TODO: move to another test
        browser.element('#movie').should(have.css_class(('active')))
        browser.element('.search_results .movie').should(
            have.exact_text('There are no movies that matched your query.')
        )

    def should_have_menu_tabs_active_with_texts(self):
        pass
