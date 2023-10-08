from themoviedb_tests.pages.movie_page import MoviePage
from themoviedb_tests.data.movies import fight_club


def test_logged_out_user_can_not_add_movie_to_favorites():
    # ACT
    page = MoviePage(fight_club.id)
    page.open()
    page.should_have_favorite_button_disabled()
    page.add_to_favorites()
    # ASSERT
    page.should_not_have_favorite_button_selected()


def test_logged_in_user_can_add_movie_to_favorites(logged_in, clear_favorites):
    # ACT
    page = MoviePage(fight_club.id)
    page.open()
    page.should_have_favourite_button_enabled()
    page.add_to_favorites()
    # ASSERT
    page.should_have_favorite_button_selected()
    page.should_have_added_to_favorites(fight_club)


def test_logged_in_user_can_remove_movie_from_favorites(logged_in, clear_favorites):
    # ACT
    page = MoviePage(fight_club.id)
    page.open()
    page.add_to_favorites()
    page.remove_from_favorites()
    # ASSERT
    page.should_not_have_favorite_button_selected()
    page.should_not_have_added_to_favorites()
