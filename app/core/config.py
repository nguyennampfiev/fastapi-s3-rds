#from pydantic import BaseSettings, Field
from pydantic_settings import BaseSettings
from pydantic import Field
# from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = Field("fastapi-s3-rds", env="APP_NAME")
    DEBUG: bool = False

    database_url: str = Field(..., env="DATABASE_URL")
    aws_access_key_id: str = Field(..., env="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str = Field(..., env="AWS_SECRET_ACCESS_KEY")
    s3_bucket_name: str = Field(..., env="S3_BUCKET_NAME")
    aws_region: str = Field(..., env="AWS_REGION")

    # Presigned URL expiration time in seconds
    PRESIGNED_URL_EXPIRATION: int = Field(
        3600, description="Expiration time for presigned URLs in seconds"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
