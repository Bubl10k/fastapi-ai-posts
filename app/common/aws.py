from pydantic_settings import BaseSettings


class AwsSettings(BaseSettings):
    AWS_ACCESS_KEY: str
    AWS_SECRET_KEY: str
    AWS_REGION: str
    AWS_S3_BUCKET_NAME: str
