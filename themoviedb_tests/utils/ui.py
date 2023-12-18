from selene import browser, be

import project


def close_cookies_banner():
    accept_cookies_button = '#onetrust-accept-btn-handler'
    if browser.element(accept_cookies_button)\
            .with_(timeout=project.config.selene_timeout)\
            .wait_until(be.visible):
        browser.element(accept_cookies_button).click()
