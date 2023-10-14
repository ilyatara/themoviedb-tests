import allure
from selene import browser, be, have

import project
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

    def open(self):
        with allure.step('Open login page'):
            browser.open(self.url)

    def send_username_and_password(self, username, password):
        with allure.step(f"Send login credentials: "
                         f"username='{username}', password='{password}'"):
            self.username_input.type(username)
            self.password_input.type(password)
            self.submit_button.click()

    def should_have_warning_visible(self, errors_count=2):
        with allure.step('Check that form validation errors are visible'):
            self.warning.should(be.visible)
            self.warning_header.should(have.text('There was a problem'))
            self.warning_errors.should(have.size(errors_count))

    def should_have_user_logged_in(self):
        with allure.step('Check that user is redirected to profile'):
            profile_page = ProfilePage()
            profile_url = project.config.tmdb_base_web_url + profile_page.url
            assert browser.driver.current_url == profile_url
            profile_page.should_have_user_logged_in()

    def should_have_user_logged_out(self):
        with allure.step('Check that user is logged out'):
            self.header_profile_link.should(be.not_.present)

    def should_have_contents_visible(self):
        with allure.step('Check the contents of login page'):
            self.page_header.should(be.visible)
            self.username_input.should(be.visible)
            self.password_input.should(be.visible)
            self.submit_button.should(be.visible)
            self.reset_password_link.should(be.visible)
            self.warning.should(be.not_.visible)
