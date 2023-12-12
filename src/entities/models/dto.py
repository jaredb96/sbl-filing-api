from typing import List
from pydantic import BaseModel, ConfigDict


class RecordDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    record: int
    data: str


class ValidationResultDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    validation_id: str
    field_name: str
    severity: str
    records: List[RecordDTO] = []


class SubmissionDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    submission_id: str
    lei: str
    submitter: str
    results: List[ValidationResultDTO] = []
