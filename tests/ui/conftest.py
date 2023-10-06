import os
import urllib

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selene import browser

import project
from themoviedb_tests.utils import attach


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

    attach.add_html(browser)
    attach.add_screenshot(browser)
    attach.add_logs(browser)

    if project.config.context == 'selenoid':
        attach.add_video(browser)

    browser.quit()


@pytest.fixture(scope='function', autouse=True)
def set_language_preference():
    cookie = '{"adult":false,"i18n_fallback_language":"","locale":"en-US",' \
             '"country_code":"US","timezone":"America/New_York"}'
    cookie_encoded = urllib.parse.quote(cookie)
    browser.open(project.config.tmdb_base_web_url)
    browser.driver.add_cookie({'name': 'tmdb.prefs', 'value': cookie_encoded})
