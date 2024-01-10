from s3 import upload


async def upload_to_storage(lei: str, submission_id: str, content: bytes):
    # implement uploading process here
    upload(lei, submission_id, content)


async def validate_submission(lei: str, submission_id: str, content: bytes):
    # implement validation process here
    pass
