import pandas as pd
from services import submission_processor
from fastapi import HTTPException
import pytest
from unittest.mock import Mock, ANY
from pytest_mock import MockerFixture
from config import FsProtocol, settings
from services.submission_processor import upload_to_storage


class TestSubmissionProcessor:
    @pytest.fixture
    def mock_fs(self, mocker: MockerFixture) -> Mock:
        fs_mock_patch = mocker.patch("services.submission_processor.AbstractFileSystem")
        return fs_mock_patch.return_value

    @pytest.fixture
    def mock_fs_func(self, mocker: MockerFixture, mock_fs: Mock) -> Mock:
        fs_func_mock = mocker.patch("services.submission_processor.filesystem")
        fs_func_mock.return_value = mock_fs
        return fs_func_mock

    async def test_upload(self, mocker: MockerFixture, mock_fs_func: Mock, mock_fs: Mock):
        with mocker.mock_open(mock_fs.open):
            await upload_to_storage("test", "test", b"test content local")
        mock_fs_func.assert_called()
        mock_fs.mkdirs.assert_called()
        mock_fs.open.assert_called_with(ANY, "wb")
        file_handle = mock_fs.open()
        file_handle.write.assert_called_with(b"test content local")

    async def test_upload_s3_no_mkdir(self, mocker: MockerFixture, mock_fs_func: Mock, mock_fs: Mock):
        default_fs_proto = settings.upload_fs_protocol
        settings.upload_fs_protocol = FsProtocol.S3
        with mocker.mock_open(mock_fs.open):
            await upload_to_storage("test", "test", b"test content s3")
        mock_fs_func.assert_called()
        mock_fs.mkdirs.assert_not_called()
        mock_fs.open.assert_called_with(ANY, "wb")
        file_handle = mock_fs.open()
        file_handle.write.assert_called_with(b"test content s3")
        settings.upload_fs_protocol = default_fs_proto

    async def test_upload_failure(self, mocker: MockerFixture, mock_fs_func: Mock, mock_fs: Mock):
        log_mock = mocker.patch("services.submission_processor.log")
        mock_fs.mkdirs.side_effect = IOError("test")
        with pytest.raises(Exception) as e:
            await upload_to_storage("test", "test", b"test content")
        log_mock.error.assert_called_with("Failed to upload file", ANY, exc_info=True, stack_info=True)
        assert isinstance(e.value, HTTPException)

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

    async def test_upload_to_storage_and_update_submission(
        self, mocker: MockerFixture, mock_fs_func: Mock, mock_fs: Mock
    ):
        mock_upload_to_storage = mocker.patch("services.submission_processor.upload_to_storage")
        mock_upload_to_storage.return_value = None
        mock_update_submission = mocker.patch("services.submission_processor.update_submission")
        mock_update_submission.return_value = None
        await submission_processor.upload_to_storage_and_update_submission("test", "test", b"test content")
        assert mock_update_submission.mock_calls[0].args[0].state == "SUBMISSION_UPLOADED"
