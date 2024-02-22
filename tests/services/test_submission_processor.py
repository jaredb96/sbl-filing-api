from pytest_mock import MockerFixture
import pandas as pd

from src.services import submission_processor
from entities.models import SubmissionDAO


class TestSubmissionProcessor:
    async def test_validate_and_update(self, mocker: MockerFixture):
        mock_validation = mocker.patch("services.submission_processor.validate_phases")
        mock_validation.return_value = (True, pd.DataFrame(columns=[], index=[]))
        mock_update_submission = mocker.patch("entities.repos.submission_repo.update_submission")
        mock_update_submission.return_value = SubmissionDAO(
            submitter=1,
            state='VALIDATION_SUCCESSFUL',
            validation_ruleset_version='0.1.0',
            validation_json='{}',
            filing=None,
            confirmation_id=None
        )
        res = await submission_processor.validate_and_update_submission(pd.DataFrame(), '123456790', '1', '0.1.0')
        pass
