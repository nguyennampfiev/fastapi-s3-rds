import os
from uuid import uuid4
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.crud import file as crud_file
from app.services import s3 as s3_s3svc
from app.core.config import settings
from app.schemas.file import FileOut

router = APIRouter(prefix="/v1/files", tags=["files"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=FileOut, status_code=status.HTTP_201_CREATED)
async def upload(file: UploadFile = File(...), db: Session = Depends(get_db)):
    orig_name = file.filename or "uploaded"
    _, ext = os.path.splitext(orig_name)
    # key = f"{uuid4().hex}{ext}"

    file_id = str(uuid4())
    s3_key = f"{file_id}_{file.filename}"

    # determine size: move to end then back to start
    try:
        file.file.seek(0, os.SEEK_END)
        # size = file.file.tell()
        file.file.seek(0)
    except Exception as e:
        print(f"Could not determine file size: {e}")
        # size = None

    # upload to S3
    try:
        s3_s3svc.upload_file_to_s3(
            file.file, settings.S3_BUCKET, key=s3_key, content_type=file.content_type
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to upload file to S3: {str(e)}"
        )

    db_file = crud_file.create_file(
        db=db, file_id=file_id, filename=file.filename, s3_key=s3_key
    )

    download_url = s3_s3svc.generate_presigned_url(
        settings.S3_BUCKET, s3_key, expiration=settings.PRESIGNED_URL_EXPIRATION
    )

    return FileOut(
        id=db_file.id,
        filename=db_file.filename,
        s3_key=db_file.s3_key,
        content_type=file.content_type,
        size=db.size,
        uploaded_at=db_file.uploaded_at,
        download_url=download_url,
    )
