from selene import browser, be, have, by

from themoviedb_tests import utils
from themoviedb_tests.pages.profile_page import ProfilePage


class MoviePage:
    favorite_button = browser.element('#favourite')

    def __init__(self, id):
        self.id = id
        self.url = f'/movie/{id}'

    def open(self):
        browser.open(self.url)
        utils.ui.close_cookies_banner()

    def add_to_favorites(self):
        self.favorite_button.click()

    def remove_from_favorites(self):
        self.favorite_button.click()

    def should_have_favorite_button_selected(self):
        self.favorite_button.element('span').should(have.css_class(('true')))

    def should_not_have_favorite_button_selected(self):
        self.favorite_button.element('span').should(have.no.css_class(('true')))

    def should_have_favourite_button_enabled(self):
        self.favorite_button.hover()
        browser.all('.k-tooltip-content').element_by(
            have.exact_text('Mark as favorite')
        ).should(be.visible)

    def should_have_favorite_button_disabled(self):
        self.favorite_button.hover()
        browser.all('.k-tooltip-content').element_by(
            have.exact_text('Login to add this movie to your favorite list')
        ).should(be.visible)

    def should_not_have_added_to_favorites(self):
        profile = ProfilePage()
        profile.should_not_have_movie_in_favorites()

    def should_have_added_to_favorites(self, movie):
        profile = ProfilePage()
        profile.should_have_movie_in_favorites(movie)
