import urllib

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selene import browser

import project
from themoviedb_tests import utils


TMDB_AUTH_COOKIE_NAME = 'tmdb.session'
TMDB_PREFS_COOKIE_NAME = 'tmdb.prefs'


@pytest.fixture(scope='function', autouse=True)
def setup_browser(request):
    browser.config.base_url = project.config.tmdb_base_web_url
    browser.config.timeout = project.config.selene_timeout

    width, height = project.config.browser_size.split('x')
    browser.config.window_width = width
    browser.config.window_height = height

    if project.config.context == 'selenoid':

        if project.config.browser == 'chrome':
            options = ChromeOptions()
        elif project.config.browser == 'firefox':
            options = FirefoxOptions()

        selenoid_capabilities = {
            "browserName": project.config.browser,
            "browserVersion": project.config.browser_version,
            "selenoid:options": {
                "enableVNC": True,
                "enableVideo": True
            }
        }
        options.capabilities.update(selenoid_capabilities)

        login = project.config.selenoid_login
        password = project.config.selenoid_password
        protocol = project.config.selenoid_base_url.split('://')[0]
        domain = project.config.selenoid_base_url.split('://')[1]
        driver = webdriver.Remote(
            command_executor=f"{protocol}://{login}:{password}@{domain}/wd/hub",
            options=options
        )
        browser.config.driver = driver

    elif project.config.context == 'local':
        browser.config.driver_name = project.config.browser

    yield browser

    utils.attach.add_html(browser)
    utils.attach.add_screenshot(browser)
    utils.attach.add_logs(browser)

    if project.config.context == 'selenoid':
        utils.attach.add_video(browser)

    browser.quit()


@pytest.fixture(scope='function', autouse=True)
def set_language_preference(setup_browser):
    browser = setup_browser
    cookie = '{"adult":false,"i18n_fallback_language":"","locale":"en-US",' \
             '"country_code":"US","timezone":"America/New_York"}'
    cookie_encoded = urllib.parse.quote(cookie)
    browser.open(project.config.tmdb_base_web_url)
    browser.driver.add_cookie({'name': TMDB_PREFS_COOKIE_NAME, 'value': cookie_encoded})
    utils.ui.close_cookies_banner()


@pytest.fixture(scope='function', autouse=False)
def logged_in(setup_browser):
    browser = setup_browser
    if project.config.tmdb_auth_cookie is None:
        browser.open(project.config.tmdb_base_web_url + '/login')
        utils.ui.close_cookies_banner()
        browser.element('#username').type(project.config.tmdb_login)
        browser.element('#password').type(project.config.tmdb_password)
        browser.element('#login_button').click()
        cookie = browser.driver.get_cookie(TMDB_AUTH_COOKIE_NAME)['value']
        project.config.tmdb_auth_cookie = cookie
    else:
        browser.driver.add_cookie(
            {'name': TMDB_AUTH_COOKIE_NAME,
             'value': project.config.tmdb_auth_cookie}
        )
    yield
    browser.driver.delete_cookie(TMDB_AUTH_COOKIE_NAME)


@pytest.fixture(scope='function', autouse=False)
def clear_favorites():
    utils.api.delete_all_favorites()
    yield
    utils.api.delete_all_favorites()
