from pydantic_settings import BaseSettings
from pydantic import Field, field_validator


class Settings(BaseSettings):
    app_name: str = "Beauty Clinic API"
    database_url: str = Field(..., env="DATABASE_URL")
    jwt_secret: str = Field(..., env="JWT_SECRET")
    jwt_algorithm: str = Field("HS256", env="JWT_ALGORITHM")
    jwt_expires_minutes: int = Field(60, env="JWT_EXPIRES_MINUTES")
    cors_origins: list[str] = Field(default=["http://localhost:5173"], env="CORS_ORIGINS")
    environment: str = Field("local", env="ENVIRONMENT")

    @field_validator("cors_origins", mode="before")
    @classmethod
    def split_cors(cls, v: str | list[str]) -> list[str]:
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    class Config:
        env_file = ".env"


settings = Settings()
