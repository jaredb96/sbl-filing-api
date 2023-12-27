from datetime import datetime
from enum import Enum
from typing import get_args, List, Any, Literal
from sqlalchemy import ForeignKey, func, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.types import JSON

Severity = Literal["error", "warning"]

class SubmissionState(Enum):
    SUBMISSION_UPLOADED = 1
    SUBMISSION_UPLOAD_FAILED = 2  # This seems to only be applicable if the storage to the S3 fails.  Otherwise, if there is a failure to send the file to the initial upload endpoint, the endpoint wouldn't know about it.  
                                  # Does not being able to store to S3 indicate an overall processing failure?
    SUBMISSION_WITH_ERRORS = 3  
    SUBMISSION_WITH_WARNINGS = 4
    SUBMISSION_SUCCESSFUL = 5
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


class AuditMixin(object):
    event_time: Mapped[datetime] = mapped_column(server_default=func.now())


class SubmissionDAO(AuditMixin, Base):
    __tablename__ = "submission"
    id: Mapped[str] = mapped_column(index=True, primary_key=True)
    submitter: Mapped[str] # user_id instead?
    results: Mapped[List["FindingDAO"]] = relationship(back_populates="submission")
    state: Mapped[SubmissionState] = mapped_column(Enum(SubmissionState))
    validation_ruleset_version: Mapped[str]
    json_dump: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=True)
    filing: Mapped[str] = mapped_column(ForeignKey("filing.id"))
    def __str__(self):
        return f"Submission ID: {self.submission_id}, Submitter: {self.submitter}, LEI: {self.lei}"


class FindingDAO(AuditMixin, Base):
    __tablename__ = "submission_finding"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    submission_id: Mapped[str] = mapped_column(ForeignKey("submission.id"))
    submission: Mapped["SubmissionDAO"] = relationship(back_populates="results")  # if we care about bidirectional
    validation_code: Mapped[str]
    severity: Mapped[Severity] = mapped_column(Enum(*get_args(Severity)))
    records: Mapped[List["RecordDAO"]] = relationship(back_populates="result")


class RecordDAO(AuditMixin, Base):
    __tablename__ = "submission_finding_record"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    result_id: Mapped[str] = mapped_column(ForeignKey("submission_finding.id"))
    result: Mapped["FindingDAO"] = relationship(back_populates="records")  # if we care about bidirectional
    record: Mapped[int]
    field_name: Mapped[str]
    field_value: Mapped[str]

class FilingPeriodDAO(AuditMixin, Base):
    __tablename__ = "filing_period"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    start: Mapped[datetime]
    end: Mapped[datetime]
    due: Mapped[datetime]
    filing_type: Mapped[FilingType] = mapped_column(Enum(FilingType))

class FilingDAO(AuditMixin, Base):
    __tablename__ = "filing"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    lei: Mapped[str]
    state: Mapped[FilingState] = mapped_column(Enum(FilingState))
    filing_period = Mapped[str] = mapped_column(ForeignKey("filing_period.id"))
    institution_snapshot_id = Mapped[str] # not sure what this is