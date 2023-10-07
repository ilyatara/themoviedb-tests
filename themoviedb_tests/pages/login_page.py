from selene import browser, be, have

import project
from themoviedb_tests import utils
from themoviedb_tests.pages.profile_page import ProfilePage


class LoginPage:
    url = '/login'
    page_header = browser.element('.wrapper h2')
    username_input = browser.element('#username')
    password_input = browser.element('#password')
    submit_button = browser.element('#login_button')
    reset_password_link = browser.element('.reset a')
    warning = browser.element('.error_status')
    warning_header = browser.element('.error_status a')
    warning_errors = browser.all('.error_status li')
    header_profile_link = browser.element(
        f'.user a[href=/u/{project.config.tmdb_login}"]'
    )
    accept_cookies_button = browser.element('#onetrust-accept-btn-handler')

    def open(self):
        browser.open(self.url)
        utils.ui.close_cookies_banner()

    def send_username_and_password(self, username, password):
        self.username_input.type(username)
        self.password_input.type(password)
        self.submit_button.click()

    def should_have_warning_visible(self, errors_count=2):
        self.warning.should(be.visible)
        self.warning_header.should(have.text('There was a problem'))
        self.warning_errors.should(have.size(errors_count))

    def should_have_user_logged_in(self):
        profile_page = ProfilePage()
        profile_page.should_have_user_logged_in()

    def should_have_user_logged_out(self):
        self.header_profile_link.should(be.not_.present)

    def should_have_content_visible(self):
        self.page_header.should(be.visible)
        self.username_input.should(be.visible)
        self.password_input.should(be.visible)
        self.submit_button.should(be.visible)
        self.reset_password_link.should(be.visible)
        self.warning.should(be.not_.visible)
