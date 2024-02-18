import time

import allure
from selene import browser, be, have

import project
from themoviedb_tests.pages.profile_page import ProfilePage


class MoviePage:
    favorite_button = browser.element('#favourite')
    tooltips = browser.all('.k-tooltip-content')

    def __init__(self, id):
        self.id = id
        self.url = f'/movie/{id}'

    def open(self):
        with allure.step('Open movie page'):
            browser.open(self.url)

    def add_to_favorites(self):
        with allure.step('Add movie to favorites'):
            self.favorite_button.click()

    def remove_from_favorites(self):
        with allure.step('Remove movie from favorites'):
            self.favorite_button.click()

    def should_have_favorite_button_selected(self):
        with allure.step('Check that add-to-favorites button is selected'):
            self.favorite_button.element('span').should(have.css_class('true'))

    def should_not_have_favorite_button_selected(self):
        with allure.step('Check that add-to-favorites button is not selected'):
            self.favorite_button.element('span').should(have.no.css_class('true'))

    def should_have_favorite_button_enabled(self):
        with allure.step('Check that add-to-favorites button is enabled'):
            self.favorite_button.hover()
            self.tooltips.element_by(
                have.exact_text('Mark as favorite')
            ).should(be.visible)

    def should_have_favorite_button_disabled(self):
        with allure.step('Check that add-to-favorites button is disabled'):
            self.favorite_button.hover()
            self.tooltips.element_by(
                have.exact_text('Login to add this movie to your favorite list')
            ).should(be.visible)

    def should_have_added_to_favorites(self, movie):
        with allure.step('Check that movie was added to favorites'):
            profile = ProfilePage()
            time.sleep(project.config.selene_timeout)
            profile.should_have_movie_in_favorites(movie)

    def should_not_have_added_to_favorites(self):
        with allure.step('Check that movie wasn\'t added to favorites'):
            profile = ProfilePage()
            # wait for changes to apply
            time.sleep(project.config.selene_timeout)
            profile.should_not_have_movie_in_favorites()
