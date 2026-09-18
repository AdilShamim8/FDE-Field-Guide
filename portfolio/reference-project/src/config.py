"""
Configuration management for ETISE enterprise application.
Loaded defensively via environment variables using Pydantic Settings.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    app_name: str = "ETISE-Enterprise-Triage"
    environment: str = "development"
    log_level: str = "INFO"
    confidence_threshold: float = 0.85
    strict_grounding_refusal: bool = True
    idempotency_ttl_seconds: int = 86400
    api_secret_key: str = "dev-secret-key-change-in-production"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = AppSettings()
