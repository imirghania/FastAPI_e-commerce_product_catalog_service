from pydantic_settings import BaseSettings, SettingsConfigDict

from typing import Literal
from functools import lru_cache


@lru_cache
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', 
                                    env_file_encoding='utf-8')
    environment: Literal["dev", "test", "prod"]
    mongo_url: str
    db_name: str
    test_db_name: str


settings = Settings()