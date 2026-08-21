from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings, extra="ignore"):
    development: bool = False
    listen_host: str = "0.0.0.0"
    listen_port: int = 8000

    log_dir: str = "logs"
    log_level: str = "INFO"
    log_max_bytes: int = 10 * 1024 * 1024
    log_backup_count: int = 5
    log_to_console: bool = True

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
