from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """
    Central configuration for ARIA framework.
    Reads from .env file automatically.
    Access anywhere with: from aria.config import settings
    """

    # Target application URLs
    base_url: str = Field(default="https://automationexercise.com")
    api_base_url: str = Field(default="https://reqres.in/api")

    # Browser behaviour
    browser: str = Field(default="chromium")
    headless: bool = Field(default=False)
    slow_mo: int = Field(default=0)

    # AI integration (used from Day 5 onwards)
    openai_api_key: str = Field(default="")

    # Logging level
    log_level: str = Field(default="INFO")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Create ONE instance — import this everywhere, don't create new Settings() each time
settings = Settings()