import allure
from selene import browser, be, have

import project


class ProfilePage:
    url = f'/u/{project.config.tmdb_login}'
    favorites_url = url + '/favorites'
    menu_items = browser.all('#new_shortcut_bar > li')
    header_profile_link = browser.element(
        f'.user a[href="/u/{project.config.tmdb_login}"]'
    )
    logged_in_menu_items_count = 5
    logged_out_menu_items_count = 2
    favorites_container = browser.element('.items_wrapper')

    def open_favorites(self):
        with allure.step('Open favorites section of profile page'):
            browser.open(self.favorites_url)

    def should_have_user_logged_in(self):
        with allure.step('Check that user is logged in'):
            self.menu_items.should(have.size(self.logged_in_menu_items_count))
            self.header_profile_link.should(be.visible)

    def should_have_user_logged_out(self):
        with allure.step('Check that user is logged out'):
            self.menu_items.should(have.size(self.logged_out_menu_items_count))
            self.header_profile_link.should(be.not_.visible)

    def should_have_movie_in_favorites(self, movie):
        with allure.step('Check that movie is present in favorites list'):
            self.open_favorites()
            self.favorites_container.all('div[id^=card_movie_]')[0].element('.title h2')\
                .should(have.exact_text(movie.title))

    def should_not_have_movie_in_favorites(self):
        with allure.step('Check that favorites list is empty'):
            self.open_favorites()
            self.favorites_container.should(
                have.exact_text(("You haven't added any favorite TV shows.")))
