from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    deta_project_key = str
    deta_project_id = str

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
