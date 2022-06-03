from typing import Optional
from pydantic import BaseSettings
from os import environ


class DevSettings(BaseSettings):
    # load config from .env file
    TIMEZONE: Optional[str] = None
    DATABASE_URL: Optional[str] = None
    CSV_PATH: Optional[str] = None

    class Config:
        env_file: str = ".env.dev"


class TestSettings(BaseSettings):
    # load config from .env file
    TIMEZONE: Optional[str] = None
    DATABASE_URL: Optional[str] = None

    class Config:
        env_file: str = ".env.test"


def get_settings() -> Optional[BaseSettings]:
    env = 'dev'
    if "codefoo-env" in environ:
        env = environ["codefoo-env"]

    if env == 'dev':
        return DevSettings()
    elif env == 'test':
        return TestSettings()
    else:
        return None
