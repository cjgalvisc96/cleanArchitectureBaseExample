from typing import List

import pytest

from rentomatic.domain.room import Room
from tests.utils.faker_data import faker_data


@pytest.fixture
def get_random_domain_rooms() -> List[Room]:
    random_domain_rooms = []
    for _ in range(5):
        temp_room = Room(
            code=faker_data.uuid4(),
            size=faker_data.random_number(digits=3),
            price=faker_data.random_number(digits=3),
            longitude=float(faker_data.longitude()),
            latitude=float(faker_data.latitude()),
        )
        random_domain_rooms.append(temp_room)
    return random_domain_rooms
