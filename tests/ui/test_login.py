from selene import browser, be, have


def test_login_with_invalid_password():
    # ACT
    browser.open('/login')
    browser.element('#username').type(project.config.tmdb_login)
    browser.element('#password').type(project.config.tmdb_password[::-1])
    browser.element('#login_button').click()
    # ASSERT
    browser.element('.error_status').should(be.visible)
    browser.all('.error_status a').should(have.text('There was a problem'))
    browser.all('.error_status li').should(have.size(2))


def test_login_with_empty_username():
    # ACT
    browser.open('/login')
    browser.element('#password').type(project.config.tmdb_password)
    browser.element('#login_button').click()
    # ASSERT
    browser.element('.error_status').should(be.visible)
    browser.all('.error_status a').should(have.text('There was a problem'))
    browser.all('.error_status li').should(have.size(2))


def test_login_with_valid_username_and_password():
    # ACT
    browser.open('/login')
    browser.element('#username').type(project.config.tmdb_login)
    browser.element('#password').type(project.config.tmdb_password)
    browser.element('#login_button').click()
    # ASSERT
    browser.element(f'li.user a[href="/u/{project.config.tmdb_login}"]').should(be.visible)



def test_login_page_contents():
    # ACT
    browser.open('/login')
    # ASSERT
    browser.element('.wrapper h2').should(be.visible)
    browser.element('#username').should(be.visible)
    browser.element('#password').should(be.visible)
    browser.element('#login_button').should(be.visible)
    browser.element('.reset a').should(be.visible)
    browser.element('.error_status').should(be.not_.visible)


# def test_open_login_page():
#     # ACT
#     browser.open('/login')
#     # ASSERT
#     browser.element('.wrapper > h2').should(have.exact_text('Login to your account'))
#
#
# def test_auth_cookie(logged_in):
#     # ACT
#     browser.open(f'/u/{project.config.tmdb_login}')
#     # ASSERT
#     browser.element(f'li.user a[href="/u/{project.config.tmdb_login}"]').should(be.present)
