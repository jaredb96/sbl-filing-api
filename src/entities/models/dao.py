from datetime import datetime
from enum import Enum
from typing import Any
from sqlalchemy import Enum as SAEnum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.types import JSON


class SubmissionState(Enum):
    SUBMISSION_UPLOADED = 1
    VALIDATION_IN_PROGRESS = 2
    VALIDATION_WITH_ERRORS = 3
    VALIDATION_WITH_WARNINGS = 4
    VALIDATION_SUCCESSFUL = 5
    SUBMISSION_SIGNED = 6


class FilingState(Enum):
    FILING_STARTED = 1
    FILING_IN_PROGRESS = 2
    FILING_COMPLETE = 3


class FilingType(Enum):
    TYPE_A = "Type_A"
    TYPE_B = "Type_B"


class Base(AsyncAttrs, DeclarativeBase):
    pass


class SubmissionDAO(Base):
    __tablename__ = "submission"
    submission_id: Mapped[int] = mapped_column(index=True, primary_key=True, autoincrement=True)
    submitter: Mapped[str]
    state: Mapped[SubmissionState] = mapped_column(SAEnum(SubmissionState))
    validation_ruleset_version: Mapped[str]
    validation_json: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=True)
    filing: Mapped[str] = mapped_column(ForeignKey("filing.id"))

    def __str__(self):
        return f"Submission ID: {self.submission_id}, Submitter: {self.submitter}, State: {self.state}, Ruleset: {self.validation_ruleset_version}, Filing: {self.filing}"


class FilingPeriodDAO(Base):
    __tablename__ = "filing_period"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    start: Mapped[datetime]
    end: Mapped[datetime]
    due: Mapped[datetime]
    filing_type: Mapped[FilingType] = mapped_column(SAEnum(FilingType))


class FilingDAO(Base):
    __tablename__ = "filing"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    lei: Mapped[str]
    state: Mapped[FilingState] = mapped_column(SAEnum(FilingState))
    filing_period: Mapped[int] = mapped_column(ForeignKey("filing_period.id"))
    institution_snapshot_id = Mapped[str]  # not sure what this is


# Commenting out for now since we're just storing the results from the data-validator as JSON.
# If we determine building the data structure for results as tables is needed, we can add these
# back in.
# class FindingDAO(Base):
#    __tablename__ = "submission_finding"
#    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#    submission_id: Mapped[str] = mapped_column(ForeignKey("submission.id"))
#    submission: Mapped["SubmissionDAO"] = relationship(back_populates="results")  # if we care about bidirectional
#    validation_code: Mapped[str]
#    severity: Mapped[Severity] = mapped_column(Enum(*get_args(Severity)))
#    records: Mapped[List["RecordDAO"]] = relationship(back_populates="result")


# class RecordDAO(Base):
#    __tablename__ = "submission_finding_record"
#    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#    result_id: Mapped[str] = mapped_column(ForeignKey("submission_finding.id"))
#    result: Mapped["FindingDAO"] = relationship(back_populates="records")  # if we care about bidirectional
#    record: Mapped[int]
#    field_name: Mapped[str]
#    field_value: Mapped[str]
