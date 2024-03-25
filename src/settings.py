from pydantic import AnyHttpUrl

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SITE_URL: AnyHttpUrl
    EMAIL: str
    PASSWORD: str
    URL_PING: AnyHttpUrl
    API_ID: int
    API_HASH: str
    CHANNEL: int
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()