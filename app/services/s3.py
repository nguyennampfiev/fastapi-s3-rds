import boto3
from botocore.config import Config
from app.core.config import settings


session = boto3.session.Session()
s3_client = session.client(
    service_name="s3",
    region_name=settings.AWS_REGION,
    config=Config(signature_version="s3v4"),
)


def upload_fileobj(file_obj, bucket: str, key: str, content_type: str) -> None:
    extra_args = {}
    if content_type:
        extra_args["ContentType"] = content_type

    s3_client.upload_fileobj(
        Fileobj=file_obj,
        Bucket=bucket,
        Key=key,
        ExtraArgs={"ContentType": content_type},
    )


def generate_presigned_url(
    bucket: str, key: str, expiration: int = settings.PRESIGNED_URL_EXPIRATION
) -> str:
    return s3_client.generate_presigned_url(
        ClientMethod="get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expiration,
    )
