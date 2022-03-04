from typing import Dict, List

import pytest

from rentomatic.domain.room import Room
from tests.utils.faker_data import faker_data


@pytest.fixture
def get_random_rooms() -> List[Room]:
    random_rooms = []
    for _ in range(5):
        temp_room = dict(
            code=faker_data.uuid4(),
            size=faker_data.random_number(digits=3),
            price=faker_data.random_number(digits=3),
            longitude=float(faker_data.longitude()),
            latitude=float(faker_data.latitude()),
        )
        random_rooms.append(Room.from_dict(_dict=temp_room))
    return random_rooms


def get_status_codes() -> Dict[str, int]:
    expected_status_codes = dict(
        HTTP_200_OK=200,
        HTTP_400_BAD_REQUEST=400,
        HTTP_404_NOT_FOUND=404,
        HTTP_500_INTERNAL_SERVER_ERROR=500,
    )
    return expected_status_codes
