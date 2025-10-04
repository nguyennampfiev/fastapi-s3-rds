from sqlalchemy.orm import Session
from app.db import models


def create_file(
    db: Session,
    *,
    filename: str,
    s3_key: str,
    content_type: str | None,
    size: int | None,
) -> models.File:
    db_obj = models.File(
        filename=filename,
        s3_key=s3_key,
        content_type=content_type,
        size=size,
        url=f"https://{s3_key}",
    )

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_file(db: Session, file_id: int) -> models.File | None:
    return db.query(models.File).filter(models.File.id == file_id).first()
