from selene import browser, be, have

import project
from themoviedb_tests.pages.login_page import LoginPage


def test_login_page_contents():
    # ACT
    page = LoginPage()
    page.open()
    # ASSERT
    page.should_have_content_visible()


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


def test_login_with_empty_password():
    # ACT
    page = LoginPage()
    page.open()
    page.send_username_and_password(project.config.tmdb_login, '')
    # ASSERT
    page.should_have_warning_visible()
    page.should_have_user_logged_out()


def test_logged_in_user_is_redirected_to_profile(logged_in):
    # ACT
    page = LoginPage()
    page.open()
    # ASSERT
    page.should_have_user_logged_in()
