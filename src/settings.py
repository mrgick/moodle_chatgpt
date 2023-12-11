from pydantic import AnyHttpUrl

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SITE_URL: AnyHttpUrl
    EMAIL: str
    PASSWORD: str
    OPENAI_KEY: str
    URL_PING: AnyHttpUrl
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()