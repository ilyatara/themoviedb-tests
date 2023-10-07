import urllib

import pytest
import themoviedb_tests.utils.attach
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selene import browser, be
import requests

import project
from themoviedb_tests import utils


@pytest.fixture(scope='function', autouse=True)
def setup_browser(request):
    browser.config.base_url = project.config.tmdb_base_web_url
    browser.config.timeout = project.config.selene_timeout

    if project.config.browser == 'chrome':
        options = ChromeOptions()
    elif project.config.browser == 'firefox':
        options = FirefoxOptions()

    if project.config.context == 'selenoid':
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
        # browser.config.driver_options = options

    yield browser

    themoviedb_tests.utils.attach.add_html(browser)
    themoviedb_tests.utils.attach.add_screenshot(browser)
    themoviedb_tests.utils.attach.add_logs(browser)

    if project.config.context == 'selenoid':
        themoviedb_tests.utils.attach.add_video(browser)

    browser.quit()


@pytest.fixture(scope='function', autouse=True)
def set_language_preference():
    if project.config.context == 'selenoid':
        return
    cookie = '{"adult":false,"i18n_fallback_language":"","locale":"en-US",' \
             '"country_code":"US","timezone":"America/New_York"}'
    cookie_encoded = urllib.parse.quote(cookie)
    browser.open(project.config.tmdb_base_web_url)
    browser.driver.add_cookie({'name': 'tmdb.prefs', 'value': cookie_encoded})


@pytest.fixture(scope='session', autouse=False)  # CHANGE TO TRUE
def save_authorization_cookie():
    # Saving and later setting only one auth cookie
    # via requests doesn't get user logged in
    # for some reason, so we log in via UI.
    # Maybe some other cookies are needed.
    # TODO: Log in using requests.

    # data = {'username': project.config.tmdb_login,
    #         'password': project.config.tmdb_password}
    # chrome_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
    #                     '(KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    # headers = {'User-Agent': chrome_user_agent}
    # response = requests.post(
    #     project.config.tmdb_base_web_url + '/login',
    #     data=data, headers=headers, allow_redirects=False
    # )
    # cookie = response.cookies.get('tmdb.session')
    # project.config.tmdb_auth_cookie = cookie
    # browser.driver.delete_cookie('tmdb.session')

    browser.open(project.config.tmdb_base_web_url + '/login')
    utils.ui.close_cookies_banner()
    browser.element('#username').type(project.config.tmdb_login)
    browser.element('#password').type(project.config.tmdb_password)
    browser.element('#login_button').click()
    project.config.tmdb_auth_cookie = browser.driver.get_cookie('tmdb.session')['value']
    browser.driver.delete_cookie('tmdb.session')

    # browser.driver.delete_all_cookies()  # doesn't log out
    # browser.open(project.config.tmdb_base_web_url + '/logout')
    # browser.element(f'li.user a[href="/u/{project.config.tmdb_login}"]').click()
    # browser.element('a[href="/logout"]').click()


@pytest.fixture(scope='function', autouse=False)
def logged_in():
    auth_cookie = project.config.tmdb_auth_cookie
    browser.open(project.config.tmdb_base_web_url)
    browser.driver.add_cookie({'name': 'tmdb.session', 'value': auth_cookie})
