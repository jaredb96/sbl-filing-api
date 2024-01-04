from datetime import datetime
from typing import Dict, Any
from pydantic import BaseModel, ConfigDict


class SubmissionDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    submission_id: int | None = None
    submitter: str
    state: str | None = None
    validation_ruleset_version: str | None = None
    validation_json: Dict[str, Any] | None = None
    filing: int


class FilingDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    lei: str
    state: str
    filing_period: int
    institution_snapshot_id: str


class FilingPeriodDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    start: datetime
    end: datetime
    due: datetime
    filing_type: str
