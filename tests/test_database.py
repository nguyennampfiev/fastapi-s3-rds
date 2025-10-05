from app.db import models
from datetime import datetime

def test_file_model_attributes():
    file = models.File(
        id=1,
        filename="example.txt",
        s3_key="uuid_example.txt",
        content_type="text/plain",
        url="https://s3.amazonaws.com/bucket/uuid_example.txt",
        size=1234,
        uploaded_at="2024-01-01T00:00:00"
    )
    assert file.id == 1
    assert file.filename == "example.txt"
    assert file.s3_key == "uuid_example.txt"
    assert file.content_type == "text/plain"
    assert file.url == "https://s3.amazonaws.com/bucket/uuid_example.txt"
    assert file.size == 1234
    assert datetime.fromisoformat(file.uploaded_at) == datetime(2024, 1, 1, 0, 0, 0)
