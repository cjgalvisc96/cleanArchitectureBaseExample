from typing import List

import pytest
from faker import Faker

from rentomatic.domain.room import Room

faker_data = Faker(locale="en_US")  # TODO: constant


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
