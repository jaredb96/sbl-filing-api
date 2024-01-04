import pandas as pd
import pytest

from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from entities.models import (
    SubmissionDAO,
    SubmissionDTO,
    FilingPeriodDAO,
    FilingDAO,
    FilingType,
    FilingState,
    SubmissionState,
)
from entities.repos import submission_repo as repo


class TestSubmissionRepo:
    @pytest.fixture(scope="function", autouse=True)
    async def setup(
        self,
        transaction_session: AsyncSession,
    ):
        filing_period = FilingPeriodDAO(
            name="FilingPeriod2024",
            start=datetime.now(),
            end=datetime.now(),
            due=datetime.now(),
            filing_type=FilingType.TYPE_A,
        )
        transaction_session.add(filing_period)

        filing = FilingDAO(
            lei="1234567890", state=FilingState.FILING_STARTED, institution_snapshot_id="Snapshot-1", filing_period=1
        )
        transaction_session.add(filing)

        submission = SubmissionDAO(
            submitter="test@cfpb.gov",
            filing=1,
            state=SubmissionState.SUBMISSION_UPLOADED,
            validation_ruleset_version="v1",
        )
        transaction_session.add(submission)

        await transaction_session.commit()

    async def test_get_submission(self, query_session: AsyncSession):
        res = await repo.get_submission(query_session, submission_id=1)
        assert res.submission_id == 1
        assert res.submitter == "test@cfpb.gov"
        assert res.filing == 1
        assert res.state == SubmissionState.SUBMISSION_UPLOADED
        assert res.validation_ruleset_version == "v1"

    async def test_add_submission(self, transaction_session: AsyncSession):
        res = await repo.upsert_submission(transaction_session, SubmissionDTO(submitter="test@cfpb.gov", filing=1))
        assert res.submission_id == 2
        assert res.submitter == "test@cfpb.gov"
        assert res.filing == 1
        assert res.state == SubmissionState.SUBMISSION_UPLOADED
        assert res.validation_ruleset_version == "v1"

    # This tests directly updating the attached DAO in a session.  Since
    # once we add a Submission we'll have reference to that attached object,
    # validation should be able to directly update the DAO state and validation
    # json without having to call repo.upsert
    async def test_update_submission(self, query_session: AsyncSession):
        res = await repo.get_submission(query_session, submission_id=1)
        res.state = SubmissionState.VALIDATION_IN_PROGRESS

        stmt = select(SubmissionDAO).filter(SubmissionDAO.submission_id == 1)
        new_res1 = await query_session.scalar(stmt)
        assert new_res1.submission_id == 1
        assert new_res1.filing == 1
        assert new_res1.state == SubmissionState.VALIDATION_IN_PROGRESS

        validation_json = self.get_error_json()
        res.validation_json = validation_json
        res.state = SubmissionState.VALIDATION_WITH_ERRORS

        stmt = select(SubmissionDAO).filter(SubmissionDAO.submission_id == 1)
        new_res2 = await query_session.scalar(stmt)
        assert new_res2.submission_id == 1
        assert new_res2.filing == 1
        assert new_res2.state == SubmissionState.VALIDATION_WITH_ERRORS
        assert new_res2.validation_json == validation_json

    # This tests the upsert merge function instead of directly updating
    # the attached DAO in the session.  This is in case it's preferred to
    # call upsert on each DAO update.  Depends on if the plan is to pass around
    # the session or get a new one on each update.
    async def test_upsert_submission(self, transaction_session: AsyncSession):
        updated_sub = SubmissionDAO(
            submission_id=1,
            validation_json={},
            submitter="test@cfpb.gov",
            filing=1,
            state=SubmissionState.SUBMISSION_SIGNED,
            validation_ruleset_version="v1",
        )
        await repo.upsert_submission(transaction_session, updated_sub)

        stmt = select(SubmissionDAO).filter(SubmissionDAO.submission_id == 1)
        new_res2 = await transaction_session.scalar(stmt)
        assert new_res2.submission_id == 1
        assert new_res2.filing == 1
        assert new_res2.state == SubmissionState.SUBMISSION_SIGNED
        assert new_res2.validation_json == {}

    def get_error_json(self):
        df_columns = [
            "record_no",
            "field_name",
            "field_value",
            "validation_severity",
            "validation_id",
            "validation_name",
            "validation_desc",
        ]
        df_data = [
            [
                0,
                "uid",
                "BADUID0",
                "error",
                "E0001",
                "id.invalid_text_length",
                "'Unique identifier' must be at least 21 characters in length.",
            ],
            [
                0,
                "uid",
                "BADTEXTLENGTH",
                "error",
                "E0100",
                "ct_credit_product_ff.invalid_text_length",
                "'Free-form text field for other credit products' must not exceed 300 characters in length.",
            ],
            [
                1,
                "uid",
                "BADUID1",
                "error",
                "E0001",
                "id.invalid_text_length",
                "'Unique identifier' must be at least 21 characters in length.",
            ],
        ]
        error_df = pd.DataFrame(df_data, columns=df_columns)
        return error_df.to_json()
