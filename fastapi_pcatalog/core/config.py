from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


@lru_cache
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', 
                                    env_file_encoding='utf-8')
    mongo_url: str


settings = Settings()