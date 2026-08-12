

from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    app_name: str = "HRMS"

    database_host: str
    database_port: int
    database_name: str
    database_user: str
    database_password: str

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int =30


    model_config = SettingsConfigDict(
        env_file="backend/.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()