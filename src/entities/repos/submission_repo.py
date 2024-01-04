from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from entities.models import SubmissionDAO, SubmissionDTO, SubmissionState


async def get_submission(session: AsyncSession, submission_id: int) -> SubmissionDAO:
    async with session.begin():
        stmt = select(SubmissionDAO).filter(SubmissionDAO.submission_id == submission_id)
        return await session.scalar(stmt)


async def upsert_submission(session: AsyncSession, submission: SubmissionDTO) -> SubmissionDAO:
    async with session.begin():
        # Not sure if we really need this, since once we add the Submission to the session
        # and return that DAO, all future updates to that object during validation processing
        # should automatically update the db since it's still attached.  All those updates
        # *should* be happening within a single submission session
        if submission.submission_id:
            await session.merge(submission)
        else:
            submission = SubmissionDAO(
                submitter=submission.submitter,
                state=SubmissionState.SUBMISSION_UPLOADED,
                validation_ruleset_version="v1",  # think we need a new function in the data-validator to return the version?
                filing=submission.filing,
            )
            session.add(submission)
        await session.commit()
        return submission
