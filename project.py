import os
from typing import Optional

from pydantic_settings import BaseSettings
from dotenv import find_dotenv, load_dotenv

from themoviedb_tests.utils.helpers import get_tmdb_account_id


class Config(BaseSettings):
    tmdb_base_api_url: str
    tmdb_api_version: str
    tmdb_base_web_url: str

    tmdb_login: str
    tmdb_password: str
    tmbd_read_access_token: str
    tmdb_account_id: Optional[str] = None

    movie_rate_value: float = 8.5


config = Config(_env_file=find_dotenv('.env'))
config.tmdb_account_id = get_tmdb_account_id()
