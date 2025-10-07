import os
print("ENV VARS:", {k: os.environ.get(k) for k in ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "S3_BUCKET_NAME", "DATABASE_URL", "AWS_REGION"]})

from fastapi import FastAPI
from app.api.v1.upload import router as upload_router
from app.core.config import settings

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)
app.include_router(upload_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
