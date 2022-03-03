import pytest

from rentomatic.repository.postgres.postgres_objects import Room

pytestmark = pytest.mark.integration


def test_dummy(pg_session):
    assert len(pg_session.query(Room).all()) == 5
