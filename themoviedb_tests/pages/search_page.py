from selene import browser, be, have


class SearchPage:
    url = '/search'
    search_input = browser.element('#search_v4')
    search_menu = browser.element('.grey_column')
    search_menu_tabs_ids = (
        '#movie, #tv, #person, #collection, #company, #keyword, #network'
    )
    search_menu_tabs = browser.all(search_menu_tabs_ids)
    searchh_menu_tabs_count = len(search_menu_tabs_ids.split(','))
    search_results_container = browser.element('.white_column')

    def open(self):
        browser.open(self.url)

    def should_have_contents_visible(self):
        self.search_input.should(be.visible)
        self.search_menu.should(be.visible)
        self.search_results_container.should(be.visible)
        self.search_menu_tabs.should(have.size(self.searchh_menu_tabs_count))
        browser.element('#movie').should(have.css_class(('active')))
        browser.element('.search_results .movie').should(
            have.exact_text('There are no movies that matched your query.')
        )
