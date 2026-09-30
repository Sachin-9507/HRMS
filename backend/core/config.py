from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "HRMS"

    jwt_algorithm: str = "HS256"
    jwt_secret: str = Field(min_length=32)

    access_token_expire_minutes: int = 30

    otp_expire_minutes: int = 5
    otp_max_attempts: int = 5

    cors_origins: str = "http://localhost:5173"

    environment: str = "development"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    @property
    def cors_origin_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]


settings = Settings()