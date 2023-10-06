from selene import browser, be, have

import project
from themoviedb_tests.pages.settings_page import SettingsPage


class LoginPage:

    def __init__(self):
        self.url = '/login'
        self.page_header = browser.element('.wrapper h2')
        self.username_input = browser.element('#username')
        self.password_input = browser.element('#password')
        self.submit_button = browser.element('#login_button')
        self.reset_password_link = browser.element('.reset a')
        self.warning = browser.element('.error_status')
        self.warning_header = browser.element('.error_status a')
        self.warning_errors = browser.all('.error_status li')
        self.header_profile_link = browser.element(
            f'.user a[href=/u/{project.config.tmdb_login}"]'
        )
        self.accept_cookies_button = browser.element('#onetrust-accept-btn-handler')

    def open(self):
        browser.open(self.url)
        if self.accept_cookies_button.with_(timeout=2).wait_until(be.visible):
            self.accept_cookies_button.click()

    def send_username_and_password(self, username, password):
        self.username_input.type(username)
        self.password_input.type(password)
        self.submit_button.click()

    def should_have_warning_visible(self, errors_count=2):
        self.warning.should(be.visible)
        self.warning_header.should(have.text('There was a problem'))
        self.warning_errors.should(have.size(errors_count))

    def should_have_user_logged_in(self):
        settings_page = SettingsPage()
        settings_page.should_have_user_logged_in()

    def should_have_user_logged_out(self):
        self.header_profile_link.should(be.not_.present)

    def should_have_content_visible(self):
        self.page_header.should(be.visible)
        self.username_input.should(be.visible)
        self.password_input.should(be.visible)
        self.submit_button.should(be.visible)
        self.reset_password_link.should(be.visible)
        self.warning.should(be.not_.visible)
