from selene import browser, be, have, query

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
    search_hints_container = browser.element('.k-animation-container')
    search_hints = search_hints_container.all('li')
    movie_search_results = search_results_container.all('div[id^=card_movie_')

    def open(self):
        browser.open(self.url)
        utils.ui.close_cookies_banner()

    def click_on_search_input(self):
        self.search_input.click()

    def click_on_search_hint(self, index=4):
        self.search_request = self.search_hints[index].get(query.text)
        self.search_hints[index].click()

    def send_search_request(self, value):
        self.search_request = value
        self.click_on_search_input()
        self.search_input.type(value).press_enter()

    def first_search_result_should_have_movie_data(
            self, title=None, release_date=None, overview=None):
        first_result = self.movie_search_results[0]
        if title is None:
            title = self.search_request
        first_result.element('h2').should(have.exact_text(title))
        if release_date is not None:
            first_result.element('.release_date').should(have.exact_text(release_date))
        if overview is not None:
            result_overview = first_result.element('.overview').get(query.text)
            assert overview[:200] == result_overview[:200]

    def should_have_search_hints_visible(self):
        self.search_hints_container.should(be.visible)
        self.search_hints.should(have.size(10))

    def should_have_contents_visible(self):
        self.search_input.should(be.visible)
        self.search_hints_container.should(be.not_.visible)
        self.search_menu.should(be.visible)
        self.search_results_container.should(be.visible)
        self.search_menu_tabs.should(
            have.size(self.search_menu_tabs_count)
        )
        self.search_menu_tabs_counters.should(
            have.exact_texts(['0'] * self.search_menu_tabs_count)
        )
        self.should_have_search_tab_active_with_text(SearchTabs.movies)

    def should_have_search_tab_active_with_text(self, search_tab):
        browser.element(search_tab.css_id).click()
        browser.element(search_tab.css_id).should(have.css_class(('active')))
        self.search_results_container.element('.search_results:not(.hide)').should(
            have.exact_text(search_tab.get_no_results_text())
        )
