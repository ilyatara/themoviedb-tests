from selene import browser, be, have

import project


def test_open_login_page():
    browser.open('/login')
    browser.element('.wrapper > h2').should(have.exact_text('Login to your account'))
