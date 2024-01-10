import boto3
from moto import mock_s3
from src.services.s3 import upload


@mock_s3
def test_upload_to_storage():
    # creating mock client
    s3 = boto3.client("s3")

    # setting variables
    lei = "TESTLEI"
    submission_id = "test_submission_id"
    content = bytes("Test content", "utf-8")

    result = upload(lei, submission_id, content, s3)
    # Verify that object was put successfully
    assert result is True
    object = s3.get_object(Bucket=lei, Key=submission_id)
    assert object["Body"].read() == content
