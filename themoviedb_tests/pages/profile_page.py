from selene import browser, be, have

import project


class ProfilePage:
    url = f'/u/{project.config.tmdb_login}'
    menu_items = browser.all('#new_shortcut_bar > li')
    header_profile_link = browser.element(
        f'.user a[href="/u/{project.config.tmdb_login}"]'
    )
    logged_in_menu_items_count = 5
    logged_out_menu_items_count = 2

    def should_have_user_logged_in(self):
        self.menu_items.should(have.size(self.logged_in_menu_items_count))
        self.header_profile_link.should(be.visible)

    def should_have_user_logged_out(self):
        self.menu_itmes.should(have.size(self.logged_out_menu_items_count))
        self.header_profile_link.should(be.not_.visible)
