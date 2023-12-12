from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

import pandas as pd
from entities.models import SubmissionDAO, ValidationResultDAO, RecordDAO


async def get_submission(session: AsyncSession, submission_id: str) -> SubmissionDAO:
    async with session.begin():
        stmt = (
            select(SubmissionDAO)
            .options(joinedload(SubmissionDAO.results).joinedload(ValidationResultDAO.records))
            .filter(SubmissionDAO.submission_id == submission_id)
        )
        return await session.scalar(stmt)

# I was thinking this would be called after calling data_validator.create_schemas.validate()
# which returns a boolean, DataFrame tuple. The DataFrame represents the results of validation.
# Not sure if we'll already have the submission info in a DTO at this time (from the endpoint call)
# so we may be able to change the submission_id, submitter, and lei into an object versus individual
# data fields.
async def add_submission(
    session: AsyncSession, submission_id: str, submitter: str, lei: str, results: pd.DataFrame
) -> SubmissionDAO:
    async with session.begin():
        findings_by_v_id_df = results.reset_index().set_index(["validation_id"])
        submission = SubmissionDAO(submission_id=submission_id, submitter=submitter, lei=lei)
        validation_results = []
        for v_id_idx, v_id_df in findings_by_v_id_df.groupby(by="validation_id"):
            v_head = v_id_df.iloc[0]
            result = ValidationResultDAO(
                validation_id=v_id_idx, field_name=v_head.at["field_name"], severity=v_head.at["validation_severity"]
            )
            records = []
            for rec_no, rec_df in v_id_df.iterrows():
                record = RecordDAO(record=rec_df.at["record_no"], data=rec_df.at["field_value"])
                records.append(record)
            result.records = records
            validation_results.append(result)
        submission.results = validation_results
        session.add(submission)

        return submission
