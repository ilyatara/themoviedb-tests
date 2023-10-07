from selene import browser, be

import project


def close_cookies_banner():
    if browser.element('#onetrust-accept-btn-handler')\
            .with_(timeout=project.config.selene_timeout)\
            .wait_until(be.visible):
        browser.element('#onetrust-accept-btn-handler').click()
