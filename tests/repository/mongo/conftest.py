import pytest
from pymongo import MongoClient

from config.config import settings
from tests.utils.utils import get_random_room_dicts


@pytest.fixture(scope="session")
def mongo_session_empty():
    client = MongoClient(settings.MONGODB_URI)
    db = client[settings.APPLICATION_DB]

    yield db

    client.drop_database(settings.APPLICATION_DB)
    client.close()


@pytest.fixture(scope="function")
def mongo_test_data():
    return get_random_room_dicts()


@pytest.fixture(scope="function")
def mongo_session(mongo_session_empty, mongo_test_data):
    collection = mongo_session_empty.rooms
    collection.insert_many(mongo_test_data)

    yield mongo_session_empty

    collection.delete_many({})
