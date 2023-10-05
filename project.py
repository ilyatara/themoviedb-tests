import os

from pydantic_settings import BaseSettings
from dotenv import find_dotenv

import utils


class Config(BaseSettings):
    tmdb_base_api_url: str
    tmdb_api_version: str
    tmdb_base_web_url: str

    tmdb_login: str
    tmdb_password: str
    tmdb_read_access_token: str


config = Config(_env_file=find_dotenv('.env'))
