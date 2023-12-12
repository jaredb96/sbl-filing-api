from typing import List

from sqlalchemy import select, func, text
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

import pandas as pd
import json

from entities.models import SubmissionDAO, ValidationResultDAO, RecordDAO


async def get_submission(session: AsyncSession, submission_id: str) -> SubmissionDAO:
    async with session.begin():
        stmt = (
            select(SubmissionDAO)
            .options(joinedload(SubmissionDAO.results).joinedload(ValidationResultDAO.records))
            .filter(SubmissionDAO.submission_id == submission_id)
        )
        return await session.scalar(stmt)


async def add_submission(
    session: AsyncSession, submission_id: str, submitter: str, lei: str, results: pd.DataFrame
) -> SubmissionDAO:
    async with session.begin():
        findings_by_v_id_df = results.reset_index().set_index(["validation_id"])
        submission = SubmissionDAO(submission_id=submission_id, submitter=submitter, lei=lei)
        validation_results = []
        for v_id_idx, v_id_df in findings_by_v_id_df.groupby(by="validation_id"):
            v_head = v_id_df.iloc[0]
            print(f"Building results for error code {v_id_idx}")
            result = ValidationResultDAO(
                validation_id=v_id_idx, field_name=v_head.at["field_name"], severity=v_head.at["validation_severity"]
            )
            records = []
            for rec_no, rec_df in v_id_df.iterrows():
                print(f"{rec_no} Rec Def: {rec_df}")
                record = RecordDAO(record=rec_df.at["record_no"], data=rec_df.at["field_value"])
                records.append(record)
            result.records = records
            validation_results.append(result)
        submission.results = validation_results
        session.add(submission)

        return submission
