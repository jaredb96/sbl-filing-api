from datetime import datetime
import json
from typing import get_args, List, Any, Literal
from sqlalchemy import ForeignKey, func, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.types import JSON

Severity = Literal["error", "warning"]


class Base(AsyncAttrs, DeclarativeBase):
    pass


class AuditMixin(object):
    event_time: Mapped[datetime] = mapped_column(server_default=func.now())


class SubmissionDAO(AuditMixin, Base):
    __tablename__ = "submission"
    submission_id: Mapped[str] = mapped_column(index=True, primary_key=True)
    submitter: Mapped[str]
    lei: Mapped[str]
    results: Mapped[List["ValidationResultDAO"]] = relationship(back_populates="submission")
    json_dump: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=True)

    def __str__(self):
        return f"Submission ID: {self.submission_id}, Submitter: {self.submitter}, LEI: {self.lei}"


class ValidationResultDAO(AuditMixin, Base):
    __tablename__ = "validation_results"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    submission_id: Mapped[str] = mapped_column(ForeignKey("submission.submission_id"))
    submission: Mapped["SubmissionDAO"] = relationship(back_populates="results")  # if we care about bidirectional
    validation_id: Mapped[str]
    field_name: Mapped[str]
    severity: Mapped[Severity] = mapped_column(Enum(*get_args(Severity)))
    records: Mapped[List["RecordDAO"]] = relationship(back_populates="result")


class RecordDAO(AuditMixin, Base):
    __tablename__ = "validation_result_record"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    result_id: Mapped[str] = mapped_column(ForeignKey("validation_results.id"))
    result: Mapped["ValidationResultDAO"] = relationship(back_populates="records")  # if we care about bidirectional
    record: Mapped[int]
    data: Mapped[str]
