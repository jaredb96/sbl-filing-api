import pandas as pd
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy import select, func

from entities.models import (
    SubmissionDAO,
    ValidationResultDAO,
    RecordDAO
) 
from entities.repos import submission_repo as repo


class TestSubmissionRepo:
    @pytest.fixture(scope="function", autouse=True)
    async def setup(
        self,
        transaction_session: AsyncSession,
    ):
        submission = SubmissionDAO(submission_id="12345",
                                   submitter="test@cfpb.gov",
                                   lei="1234567890ABCDEFGHIJ")
        results = []
        result1 = ValidationResultDAO(validation_id="E0123", field_name="uid", severity="error")
        records = []
        record1a = RecordDAO(record=1,data="empty")
        records.append(record1a)
        result1.records = records
        results.append(result1)
        submission.results = results

        transaction_session.add(submission)
        await transaction_session.commit()

    async def test_get_submission(self, query_session: AsyncSession):
        res = await repo.get_submission(query_session, submission_id="12345")
        assert res.submission_id == "12345"
        assert res.submitter == "test@cfpb.gov"
        assert res.lei == "1234567890ABCDEFGHIJ"
        assert len(res.results) == 1
        assert len(res.results[0].records) == 1
        assert res.results[0].validation_id == "E0123"
        assert res.results[0].records[0].data == "empty"
        
    async def test_add_submission(self, transaction_session: AsyncSession):
        df_columns = ["record_no", "field_name", "field_value", "validation_severity", "validation_id", "validation_name", "validation_desc"]
        df_data = [[0, "uid", "BADUID0", "error", "E0001", "id.invalid_text_length", "'Unique identifier' must be at least 21 characters in length."],
                   [0, "uid", "BADTEXTLENGTH", "error", "E0100", "ct_credit_product_ff.invalid_text_length", "'Free-form text field for other credit products' must not exceed 300 characters in length."],
                   [1, "uid", "BADUID1", "error", "E0001", "id.invalid_text_length", "'Unique identifier' must be at least 21 characters in length."]]
        error_df = pd.DataFrame(df_data, columns=df_columns)
        print(f"Data Frame: {error_df}")
        res = await repo.add_submission(transaction_session, submission_id="12346", submitter="test@cfpb.gov", lei="1234567890ABCDEFGHIJ", results=error_df)
        assert res.submission_id == "12346"
        assert res.submitter == "test@cfpb.gov"
        assert res.lei == "1234567890ABCDEFGHIJ"
        assert len(res.results) == 2 # Two error codes, 3 records total
        assert len(res.results[0].records) == 2
        assert len(res.results[1].records) == 1
        assert res.results[0].validation_id == "E0001"
        assert res.results[1].validation_id == "E0100"
        assert res.results[0].records[0].data == "BADUID0"
                                                                              