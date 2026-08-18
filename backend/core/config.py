from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "HRMS"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    jwt_secret: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()