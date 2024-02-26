from io import BytesIO

from fastapi import BackgroundTasks
from regtech_data_validator.create_schemas import validate_phases
import pandas as pd
import importlib.metadata as imeta

from entities.models import SubmissionDAO, SubmissionState
from entities.repos.submission_repo import update_submission


async def upload_to_storage(lei: str, submission_id: str, content: bytes):
    # implement uploading process here
    pass


async def validate_submission(lei: str, submission_id: str, content: bytes, background_tasks: BackgroundTasks):
    df = pd.read_csv(BytesIO(content), dtype=str, na_filter=False)
    validator_version = imeta.version("regtech-data-validator")

    # Set VALIDATION_IN_PROGRESS
    await update_submission(SubmissionDAO(submitter=submission_id, state=SubmissionState.VALIDATION_IN_PROGRESS))
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
