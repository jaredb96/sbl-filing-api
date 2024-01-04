from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from typing import List

from entities.models import SubmissionDAO, SubmissionDTO, SubmissionState


async def get_submissions(session: AsyncSession, filing_id: int = None) -> List[SubmissionDAO]:
    async with session.begin():
        stmt = select(SubmissionDAO)
        if filing_id:
            stmt = stmt.filter(SubmissionDAO.filing == filing_id)
        results = await session.scalars(stmt)
        return results.all()


async def get_submission(session: AsyncSession, submission_id: int) -> SubmissionDAO:
    async with session.begin():
        stmt = select(SubmissionDAO).filter(SubmissionDAO.submission_id == submission_id)
        return await session.scalar(stmt)


async def add_submission(session: AsyncSession, submission: SubmissionDTO) -> SubmissionDAO:
    async with session.begin():
        new_sub = SubmissionDAO(
            submitter=submission.submitter,
            state=SubmissionState.SUBMISSION_UPLOADED,
            validation_ruleset_version="v1",  # think we need a new function in the data-validator to return the version?
            filing=submission.filing,
        )
        session.add(new_sub)
        await session.commit()
        return new_sub
