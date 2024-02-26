from pytest_mock import MockerFixture
import pandas as pd

from services import submission_processor


class TestSubmissionProcessor:
    async def test_validate_and_update_successful(self, mocker: MockerFixture):
        mock_validation = mocker.patch("services.submission_processor.validate_phases")
        mock_validation.return_value = (True, pd.DataFrame(columns=[], index=[]))
        mock_update_submission = mocker.patch("services.submission_processor.update_submission")
        mock_update_submission.return_value = None
        await submission_processor.validate_and_update_submission(pd.DataFrame(), "123456790", "1", "0.1.0")
        assert mock_update_submission.mock_calls[0].args[0].state == "VALIDATION_SUCCESSFUL"

    async def test_validate_and_update_warnings(self, mocker: MockerFixture):
        mock_validation = mocker.patch("services.submission_processor.validate_phases")
        mock_validation.return_value = (False, pd.DataFrame([["warning"]], columns=["validation_severity"]))
        mock_update_submission = mocker.patch("services.submission_processor.update_submission")
        mock_update_submission.return_value = None
        await submission_processor.validate_and_update_submission(pd.DataFrame(), "123456790", "1", "0.1.0")
        assert mock_update_submission.mock_calls[0].args[0].state == "VALIDATION_WITH_WARNINGS"

    async def test_validate_and_update_errors(self, mocker: MockerFixture):
        mock_validation = mocker.patch("services.submission_processor.validate_phases")
        mock_validation.return_value = (False, pd.DataFrame([["error"]], columns=["validation_severity"]))
        mock_update_submission = mocker.patch("services.submission_processor.update_submission")
        mock_update_submission.return_value = None
        await submission_processor.validate_and_update_submission(pd.DataFrame(), "123456790", "1", "0.1.0")
        assert mock_update_submission.mock_calls[0].args[0].state == "VALIDATION_WITH_ERRORS"
