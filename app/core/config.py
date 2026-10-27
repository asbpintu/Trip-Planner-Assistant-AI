from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


class Settings(BaseSettings):
    APP_NAME: str = "Trip Planner Assistant AI"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    DEBUG: bool = True

    DB_SERVER: str = ""
    DB_INSTANCE: str = ""
    DB_NAME: str = ""
    DB_DRIVER: str = "ODBC Driver 18 for SQL Server"
    DB_TRUST_CERTIFICATE: str = "yes"
    DB_TRUSTED_CONNECTION: str = "yes"

    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "openai/gpt-oss-20b"
    GROQ_MODEL_FALLBACKS: str = "openai/gpt-oss-120b"

    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    @property
    def database_url(self):
        server = (
            f"{self.DB_SERVER}\\{self.DB_INSTANCE}"
            if self.DB_INSTANCE
            else self.DB_SERVER
        )

        return URL.create(
            "mssql+pyodbc",
            host=server,
            database=self.DB_NAME,
            query={
                "driver": self.DB_DRIVER,
                "trusted_connection": self.DB_TRUSTED_CONNECTION,
                "TrustServerCertificate": self.DB_TRUST_CERTIFICATE,
            },
        )


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()