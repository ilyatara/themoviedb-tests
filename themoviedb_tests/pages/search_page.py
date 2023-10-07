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
    search_hints_container = browser.element('.k-animation-container')

    def open(self):
        browser.open(self.url)
        utils.ui.close_cookies_banner()

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

    # def should_have_search_tabs_active_with_texts(self):
    #     for st in SearchTabs:
    #         browser.element(st.css_id).click()
    #         browser.element(st.css_id).should(have.css_class(('active')))
    #         self.search_results_container.element('.search_results:not(.hide)').should(
    #             have.exact_text(st.get_no_results_text())
    #         )
