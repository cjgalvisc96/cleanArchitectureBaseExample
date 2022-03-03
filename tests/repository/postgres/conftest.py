from typing import Any, Dict, List

import pytest
import sqlalchemy
from faker import Faker

from rentomatic.repository.postgres.postgres_objects import Base, Room

faker_data = Faker(locale="en_US")  # TODO: constant


@pytest.fixture(scope="session")
def pg_session_empty(app_configuration):
    conn_str = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
        app_configuration["POSTGRES_USER"],
        app_configuration["POSTGRES_PASSWORD"],
        app_configuration["POSTGRES_HOSTNAME"],
        app_configuration["POSTGRES_PORT"],
        app_configuration["APPLICATION_DB"],
    )
    engine = sqlalchemy.create_engine(conn_str)
    connection = engine.connect()

    Base.metadata.create_all(engine)
    Base.metadata.bind = engine

    DBSession = sqlalchemy.orm.sessionmaker(bind=engine)
    session = DBSession()

    yield session

    session.close()
    connection.close


@pytest.fixture(scope="session")
def pg_test_data() -> List[Dict[str, Any]]:
    random_pg_test_data = []
    for _ in range(5):
        temp_room = dict(
            code=faker_data.uuid4(),
            size=faker_data.random_number(digits=3),
            price=faker_data.random_number(digits=3),
            longitude=float(faker_data.longitude()),
            latitude=float(faker_data.latitude()),
        )
        random_pg_test_data.append(temp_room)
    return random_pg_test_data


@pytest.fixture(scope="function")
def pg_session(pg_session_empty, pg_test_data):
    for r in pg_test_data:
        new_room = Room(
            code=r["code"],
            size=r["size"],
            price=r["price"],
            longitude=r["longitude"],
            latitude=r["latitude"],
        )
        pg_session_empty.add(new_room)
        pg_session_empty.commit()

    yield pg_session_empty

    pg_session_empty.query(Room).delete()
