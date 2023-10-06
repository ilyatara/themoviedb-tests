from selene import browser, be, have

import project


def test_open_login_page():
    # ACT
    browser.open('/login')
    # ASSERT
    browser.element('.wrapper > h2').should(have.exact_text('Login to your account'))


def test_login_successful():
    # ACT
    browser.open('/login')
    if browser.element('#onetrust-accept-btn-handler').matching(be.present):
        browser.element('#onetrust-accept-btn-handler').click()
    browser.element('#username').type(project.config.tmdb_login)
    browser.element('#password').type(project.config.tmdb_password)
    browser.element('#login_button').click()
    # ASSERT
    browser.element(f'li.user a[href="/u/{project.config.tmdb_login}"]').should(be.visible)


def test_auth_cookie(logged_in):
    # ACT
    browser.open(f'/u/{project.config.tmdb_login}')
    # ASSERT
    browser.element(f'li.user a[href="/u/{project.config.tmdb_login}"]').should(be.present)
