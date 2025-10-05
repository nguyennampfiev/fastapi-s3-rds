import io
import pytest
from app.main import app


@pytest.fixture
def mock_db(monkeypatch):
    class DummyDBFile:
        id = 1
        filename = "test.txt"
        s3_key = "uuid_test.txt"
        content_type = "text/plain"
        size = 4
        uploaded_at = "2024-01-01T00:00:00"
    def dummy_create_file(db, filename, s3_key, content_type, size):
        return DummyDBFile()
    monkeypatch.setattr("app.crud.file.create_file", dummy_create_file)

@pytest.fixture
def mock_s3(monkeypatch):
    def dummy_upload_fileobj(fileobj, bucket, key, content_type):
        pass
    def dummy_generate_presigned_url(bucket, key, expiration):
        return f"https://s3.fake/{key}"
    monkeypatch.setattr("app.services.s3.upload_fileobj", dummy_upload_fileobj)
    monkeypatch.setattr("app.services.s3.generate_presigned_url", dummy_generate_presigned_url)

@pytest.fixture
def mock_settings(monkeypatch):
    class DummySettings:
        s3_bucket_name = "test-bucket"
        PRESIGNED_URL_EXPIRATION = 3600
    monkeypatch.setattr("app.core.config.settings", DummySettings())

def test_upload_success(client, mock_db, mock_s3, mock_settings):
    file_content = b"test"
    response = client.post(
        "/v1/files/",
        files={"file": ("test.txt", io.BytesIO(file_content), "text/plain")}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["filename"] == "test.txt"
    assert data["s3_key"].endswith("test.txt")
    assert data["content_type"] == "text/plain"
    assert data["size"] == 4
    assert data["download_url"].startswith("https://s3.fake/")

def test_upload_s3_failure(client, mock_db, mock_settings, monkeypatch):
    def fail_upload_fileobj(fileobj, bucket, key, content_type):
        raise Exception("S3 error")
    monkeypatch.setattr("app.services.s3.upload_fileobj", fail_upload_fileobj)
    file_content = b"fail"
    response = client.post(
        "/v1/files/",
        files={"file": ("fail.txt", io.BytesIO(file_content), "text/plain")}
    )
    assert response.status_code == 500
    assert "Failed to upload file to S3" in response.json()["detail"]