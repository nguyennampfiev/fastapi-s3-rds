from sqlalchemy import Column, Integer, String, DateTime, BigInteger, func
from app.db.base import Base


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True, nullable=False)
    s3_key = Column(String, unique=True, nullable=False)
    content_type = Column(String, nullable=False)
    url = Column(String, unique=True, nullable=False)
    size = Column(BigInteger, nullable=False)
    uploaded_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
