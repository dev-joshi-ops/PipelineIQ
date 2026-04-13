import sys
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr
from loguru import logger


class Settings(BaseSettings):
    """Configuration settings for the PipelineIQ Jenkins MCP."""

    jenkins_url: str = Field(..., description="Base URL of the Jenkins server")
    jenkins_user: str = Field(..., description="Username for Jenkins authentication")
    jenkins_token: SecretStr = Field(..., description="API Token for Jenkins authentication")

    # Optional settings with defaults
    request_timeout: int = Field(5, description="Timeout for Jenkins API requests in seconds")
    max_log_lines: int = Field(2000, description="Maximum number of log lines to retrieve")
    log_level: str = Field("INFO", description="Logging level")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache()
def get_settings() -> Settings:
    """Returns a cached Settings instance."""
    return Settings()


def configure_logging():
    """Configures loguru to output to stderr for MCP compatibility."""
    settings = get_settings()
    logger.remove()  # Remove default handler
    logger.add(
        sys.stderr,
        level=settings.log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    )
