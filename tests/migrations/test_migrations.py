from pytest_alembic.tests import (
    test_single_head_revision,  # noqa: F401
    test_up_down_consistency,  # noqa: F401
    test_upgrade,  # noqa: F401
)

import sqlalchemy
from sqlalchemy.engine import Engine

from pytest_alembic import MigrationContext


def test_migrations(alembic_runner: MigrationContext, alembic_engine: Engine):
    alembic_runner.migrate_up_to("af1ba24f831a")

    inspector = sqlalchemy.inspect(alembic_engine)
    tables = inspector.get_table_names()
    assert "submission" in tables
    assert {"submission_id", "submitter", "lei", "json_dump", "event_time"} == set(
        [c["name"] for c in inspector.get_columns("submission")]
    )

    assert "validation_result" in tables
    assert {"id", "submission_id", "validation_id", "field_name", "severity", "event_time"} == set(
        [c["name"] for c in inspector.get_columns("validation_result")]
    )
    vr_fk = inspector.get_foreign_keys("validation_result")[0]
    assert (
        "submission_id" in vr_fk["constrained_columns"]
        and "submission" == vr_fk["referred_table"]
        and "submission_id" in vr_fk["referred_columns"]
    )

    assert "validation_result_record" in tables
    assert {"id", "result_id", "record", "data", "event_time"} == set(
        [c["name"] for c in inspector.get_columns("validation_result_record")]
    )
    vrr_fk = inspector.get_foreign_keys("validation_result_record")[0]
    assert (
        "result_id" in vrr_fk["constrained_columns"]
        and "validation_result" == vrr_fk["referred_table"]
        and "id" in vrr_fk["referred_columns"]
    )
