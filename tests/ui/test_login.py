import allure
from allure_commons.types import Severity

import project
from themoviedb_tests.pages.login_page import LoginPage


pytestmark = [
    allure.tag('web'),
    allure.severity(Severity.CRITICAL),
    allure.label('owner', 'Ilya Tarasov'),
    allure.feature('Authorization')
]


@allure.title('Contents of the login page are displayed correctly')
def test_login_page_contents():
    # ACT
    page = LoginPage()
    page.open()
    # ASSERT
    page.should_have_contents_visible()


@allure.title('Log in with valid username and password')
def test_login_with_valid_username_and_password():
    # ACT
    page = LoginPage()
    page.open()
    page.send_username_and_password(
        project.config.tmdb_login,
        project.config.tmdb_password
    )
    # ASSERT
    page.should_have_user_logged_in()


@allure.title('Log in with invalid password')
def test_login_with_invalid_password():
    # ACT
    page = LoginPage()
    page.open()
    page.send_username_and_password(
        project.config.tmdb_login,
        project.config.tmdb_password[:-1]
    )
    # ASSERT
    page.should_have_warning_visible()
    page.should_have_user_logged_out()


@allure.title('Log in with empty password')
def test_login_with_empty_password():
    # ACT
    page = LoginPage()
    page.open()
    page.send_username_and_password(project.config.tmdb_login, '')
    # ASSERT
    page.should_have_warning_visible()
    page.should_have_user_logged_out()


@allure.title('Logged in user is redirected to profile from login page')
def test_logged_in_user_is_redirected_to_profile(logged_in):
    # ACT
    page = LoginPage()
    page.open()
    # ASSERT
    page.should_have_user_logged_in()
