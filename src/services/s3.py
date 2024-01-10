import boto3
import logging
from botocore.exceptions import ClientError


s3_client = boto3.client("s3")


def upload(bucket_name: str, filename: str, content: bytes, client: boto3.client = s3_client):
    try:
        # This is idempotent. It will only create bucket if it does not exist.
        client.create_bucket(Bucket=bucket_name)
        client.put_object(Bucket=bucket_name, Body=content, Key=filename)
    except ClientError as e:
        logging.error(e)
        return False
    return True
