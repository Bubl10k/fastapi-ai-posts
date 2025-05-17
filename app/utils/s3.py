from uuid import uuid4

import boto3
from botocore.exceptions import NoCredentialsError
from fastapi import UploadFile

from app.common.settings import settings

s3 = boto3.client(
    "s3",
    region_name=settings.aws.AWS_REGION,
    aws_access_key_id=settings.aws.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.aws.AWS_SECRET_KEY,
)


def upload_file_to_s3(file: UploadFile, user_id: int):
    try:
        file_extension = file.filename.split(".")[-1]
        key = f"avatars/user_{user_id}_{uuid4().hex}.{file_extension}"
        bucket_name = settings.aws.AWS_S3_BUCKET_NAME
        region = settings.aws.AWS_REGION

        s3.upload_fileobj(
            file.file, bucket_name, key, ExtraArgs={"ACL": "public-read", "ContentType": file.content_type}
        )

        s3_url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{key}"
        return s3_url

    except NoCredentialsError:
        raise Exception("AWS credentials not found.")
    except Exception as e:
        raise Exception(f"Upload failed: {str(e)}")
