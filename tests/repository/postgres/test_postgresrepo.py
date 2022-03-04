import pytest

from rentomatic.repository.postgres.postgres_objects import Room

pytestmark = pytest.mark.integration


def test_dummy(postgres_session):
    assert len(postgres_session.query(Room).all()) == 5
