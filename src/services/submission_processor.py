from io import BytesIO
from fastapi import BackgroundTasks
from regtech_data_validator.create_schemas import validate_phases
import pandas as pd
import importlib.metadata as imeta
from entities.models import SubmissionDAO, SubmissionState
from entities.repos.submission_repo import update_submission
from http import HTTPStatus
from fastapi import HTTPException
import logging
from fsspec import AbstractFileSystem, filesystem
from config import settings, FsProtocol

log = logging.getLogger(__name__)


async def upload_to_storage(lei: str, submission_id: str, content: bytes, extension: str = "csv"):
    try:
        fs: AbstractFileSystem = filesystem(settings.upload_fs_protocol.value)
        if settings.upload_fs_protocol == FsProtocol.FILE:
            fs.mkdirs(f"{settings.upload_fs_root}/{lei}", exist_ok=True)
        with fs.open(f"{settings.upload_fs_root}/{lei}/{submission_id}.{extension}", "wb") as f:
            f.write(content)
    except Exception as e:
        log.error("Failed to upload file", e, exc_info=True, stack_info=True)
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Failed to upload file")


async def upload_to_storage_and_update_submission(lei: str, submission_id: str, content: bytes, extension: str = "csv"):
    await upload_to_storage(lei, submission_id, content, extension)
    # Set SUBMISSION_UPLOADED
    await update_submission(SubmissionDAO(submitter=submission_id, state=SubmissionState.SUBMISSION_UPLOADED))


async def validate_submission(lei: str, submission_id: str, content: bytes, background_tasks: BackgroundTasks):
    df = pd.read_csv(BytesIO(content), dtype=str, na_filter=False)
    validator_version = imeta.version("regtech-data-validator")

    # Set VALIDATION_IN_PROGRESS
    await update_submission(
        SubmissionDAO(
            submitter=submission_id,
            state=SubmissionState.VALIDATION_IN_PROGRESS,
            validation_ruleset_version=validator_version,
        )
    )
    background_tasks.add_task(validate_and_update_submission, df, lei, submission_id, validator_version)


async def validate_and_update_submission(df: pd.DataFrame, lei: str, submission_id: str, validator_version: str):
    # Validate Phases
    result = validate_phases(df, {"lei": lei})

    # Update tables with response
    if not result[0]:
        sub_state = (
            SubmissionState.VALIDATION_WITH_ERRORS
            if "error" in result[1]["validation_severity"].values
            else SubmissionState.VALIDATION_WITH_WARNINGS
        )
        await update_submission(
            SubmissionDAO(
                submitter=submission_id,
                state=sub_state,
                validation_ruleset_version=validator_version,
                validation_json=result[1].to_json(),
            )
        )
    else:
        await update_submission(
            SubmissionDAO(
                submitter=submission_id,
                state=SubmissionState.VALIDATION_SUCCESSFUL,
                validation_ruleset_version=validator_version,
                validation_json=result[1].to_json(),
            )
        )
