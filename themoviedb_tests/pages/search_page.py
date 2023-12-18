import allure
from selene import browser, be, have, query

import project
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
    people_search_results = search_results_container.all('div.list_item')

    def open(self):
        with allure.step('Open search page'):
            browser.open(self.url)

    def click_on_search_input(self):
        with allure.step('Click on search input'):
            self.search_input.click()

    def click_on_search_hint(self, index=1):
        with allure.step('Click on search suggestion'):
            self.search_query = self.search_hints[index].get(query.text)
            self.search_hints[index].click()

    def send_search_query(self, value):
        with allure.step(f'Send search query: {value}'):
            self.search_query = value
            self.click_on_search_input()
            self.search_input.type(value).press_enter()

    def should_have_contents_visible(self):
        with allure.step('Check contents of the search page'):
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
        with allure.step(
                f'Check text in search results section for the tab: {search_tab.tab_name}'):
            browser.element(search_tab.css_id).click()
            browser.element(search_tab.css_id).should(have.css_class(('active')))
            self.search_results_container.element('.search_results:not(.hide)').should(
                have.exact_text(search_tab.get_no_results_text())
            )

    def should_have_search_hints_visible(self):
        with allure.step('Check that search suggestions are visible'):
            self.search_hints_container.should(be.visible)
            self.search_hints.should(have.size(10))

    def should_have_movie_data_in_first_search_result(
            self, title=None, release_date=None, overview=None, id_=None
    ):
        with allure.step('Check that the movie is first in search results'):
            first_result = self.movie_search_results[0]
            if title is None:
                title = self.search_query
            first_result.element('h2').should(have.exact_text(title))
            if release_date:
                first_result.element('.release_date').should(have.exact_text(release_date))
            if overview:
                result_overview = first_result.element('.overview').get(query.text)
                assert overview[:200] == result_overview[:200]
            if id_:
                expected_link = f'{project.config.tmdb_base_web_url}/movie/{id_}'
                first_result.element('.title a').should(have.attribute('href', expected_link))
                first_result.element('.image a').should(have.attribute('href', expected_link))

    def should_have_person_data_in_first_search_result(self, full_name, known_for, movies, id):
        with allure.step('Check that the person is first in search results'):
            first_result = self.people_search_results[0]
            first_result.element('.name').should(have.exact_text(full_name))
            first_result.element('.sub span').should(have.exact_text(known_for))
            for movie in movies:
                first_result.element('.sub').should(have.text(movie))
            expected_link = f'{project.config.tmdb_base_web_url}/person/{id}'
            first_result.element('.name a').should(have.attribute('href', expected_link))
            first_result.element('.image_content a').should(have.attribute('href', expected_link))
