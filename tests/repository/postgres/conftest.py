from typing import Any, Dict, List

import pytest
import sqlalchemy

from config.config import settings
from rentomatic.repository.postgres.postgres_objects import Base, RoomPostgres
from tests.utils.utils import faker_data


@pytest.fixture(scope="session")
def postgres_session_empty():
    engine = sqlalchemy.create_engine(url=settings.POSTGRES_URI)
    connection = engine.connect()

    Base.metadata.create_all(engine)
    Base.metadata.bind = engine

    DBSession = sqlalchemy.orm.sessionmaker(bind=engine)
    session = DBSession()

    yield session

    session.close()
    connection.close


@pytest.fixture(scope="session")
def postgres_test_data() -> List[Dict[str, Any]]:
    random_postgres_test_data = []
    for _ in range(settings.NUMBER_OF_RANDOM_TEST_ROOMS):
        temp_room = dict(
            code=faker_data.uuid4(),
            size=faker_data.random_number(digits=3),
            price=faker_data.random_number(digits=3),
            longitude=float(faker_data.longitude()),
            latitude=float(faker_data.latitude()),
        )
        random_postgres_test_data.append(temp_room)
    return random_postgres_test_data


@pytest.fixture(scope="function")
def postgres_session(postgres_session_empty, postgres_test_data):
    for room_test in postgres_test_data:
        temp_room_test = RoomPostgres(
            code=room_test["code"],
            size=room_test["size"],
            price=room_test["price"],
            longitude=room_test["longitude"],
            latitude=room_test["latitude"],
        )
        postgres_session_empty.add(temp_room_test)
        postgres_session_empty.commit()

    yield postgres_session_empty

    postgres_session_empty.query(RoomPostgres).delete()
