from typing import List

import pytest
from faker import Faker

from rentomatic.domain.room import Room

faker_data = Faker(locale="en_US")  # TODO: constant


@pytest.fixture
def domain_rooms() -> List[Room]:
    room_1 = dict(
        code=faker_data.uuid4(),
        size=faker_data.random_number(digits=3),
        price=faker_data.random_number(digits=3),
        longitude=faker_data.longitude(),
        latitude=faker_data.latitude(),
    )
    room_2 = dict(
        code=faker_data.uuid4(),
        size=faker_data.random_number(digits=3),
        price=faker_data.random_number(digits=3),
        longitude=faker_data.longitude(),
        latitude=faker_data.latitude(),
    )
    room_3 = dict(
        code=faker_data.uuid4(),
        size=faker_data.random_number(digits=3),
        price=faker_data.random_number(digits=3),
        longitude=faker_data.longitude(),
        latitude=faker_data.latitude(),
    )
    room_4 = dict(
        code=faker_data.uuid4(),
        size=faker_data.random_number(digits=3),
        price=faker_data.random_number(digits=3),
        longitude=faker_data.longitude(),
        latitude=faker_data.latitude(),
    )
    return [room_1, room_2, room_3, room_4]
