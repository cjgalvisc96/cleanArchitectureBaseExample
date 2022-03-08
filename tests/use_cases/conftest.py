from typing import List

import pytest

from config.config import settings
from rentomatic.domain.room import Room
from tests.utils.utils import faker_data


@pytest.fixture
def get_random_domain_rooms() -> List[Room]:
    random_domain_rooms = []
    for _ in range(settings.NUMBER_OF_RANDOM_TEST_ROOMS):
        temp_room = Room(
            code=faker_data.uuid4(),
            size=faker_data.random_number(digits=3),
            price=faker_data.random_number(digits=3),
            longitude=float(faker_data.longitude()),
            latitude=float(faker_data.latitude()),
        )
        random_domain_rooms.append(temp_room)
    return random_domain_rooms
