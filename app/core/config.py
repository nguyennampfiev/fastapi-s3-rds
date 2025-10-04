from pydantic import BaseSettings, Field

# from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = Field("fastapi-s3-rds", env="APP_NAME")
    DEBUG: bool = False

    DATABASE_URL: str

    # AWS S3 Configuration
    AWS_REGION: str
    S3_BUCKET: str

    # Presigned URL expiration time in seconds
    PRESIGNED_URL_EXPIRATION: int = Field(
        3600, description="Expiration time for presigned URLs in seconds"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
