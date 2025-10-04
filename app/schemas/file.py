from pydantic import BaseModel, HttpUrl
from datetime import datetime


class FileCreate(BaseModel):
    filename: str


class FileOut(BaseModel):
    id: int
    filename: str
    s3_key: str
    content_type: str | None
    download_url: HttpUrl
    size: int | None
    uploaded_at: datetime

    class Config:
        orm_mode = True
