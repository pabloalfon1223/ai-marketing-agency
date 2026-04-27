from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    anthropic_api_key: str = ""
    database_url: str = "sqlite+aiosqlite:///./data/agency.db"
    default_model: str = "claude-sonnet-4-20250514"
    max_concurrent_tasks: int = 3
    cors_origins: str = "http://localhost:5173"

    # Google Sheets Configuration
    google_sheets_id: str = ""
    google_credentials_path: str = "./credentials/google-credentials.json"
    google_credentials_json: str = ""  # Alternative: inline JSON credentials

    # Gmail Configuration para notificaciones
    gmail_sender_email: str = ""
    gmail_app_password: str = ""
    gmail_recipient_email: str = ""
    gmail_enabled: bool = False

    # Discord Bot Configuration
    discord_bot_token: str = ""
    discord_server_id: str = ""
    discord_cerebro_channel: str = "0"
    discord_mente_pausada_channel: str = "0"
    discord_polt_mobilier_channel: str = "0"
    discord_sistema_jefe_channel: str = "0"
    discord_pruebas_channel: str = "0"
    discord_enabled: bool = False

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
