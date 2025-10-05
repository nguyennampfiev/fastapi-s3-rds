from fastapi import FastAPI
from app.api.v1.upload import router as upload_router
from app.core.config import settings

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)
app.include_router(upload_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
