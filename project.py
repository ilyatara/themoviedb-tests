import os
from typing import Optional, Literal

from pydantic_settings import BaseSettings
from dotenv import find_dotenv, load_dotenv

from themoviedb_tests.utils.helpers import get_tmdb_account_id


class Config(BaseSettings):
    context: Literal['local', 'selenoid'] = 'local'
    tmdb_base_api_url: str
    tmdb_base_web_url: str

    tmdb_login: str
    tmdb_password: str
    tmbd_read_access_token: str
    tmdb_account_id: Optional[str] = None
    tmdb_auth_cookie: Optional[str] = None

    movie_rate_value: float = 8.5

    sleep_timeout: int = 4
    selene_timeout: int = 5

    browser: Literal['chrome', 'firefox'] = 'chrome'
    browser_version: Optional[Literal['100.0', '99.0', '98.0', '97.0']] = None

    selenoid_login: Optional[str] = None
    selenoid_password: Optional[str] = None
    selenoid_base_url: Optional[str] = None


config = Config(_env_file=find_dotenv('.env'))
# config.tmdb_account_id = get_tmdb_account_id()
config.tmdb_account_id = 20525440
