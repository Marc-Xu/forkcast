"""
Application configuration using environment variables.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Runtime settings loaded from environment or .env file.

    Attributes:
        db_url: Database connection URL.
        debug: Enable FastAPI debug mode.
    """

    db_url: str = "sqlite:///./restaurants.db"
    debug: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
    )
