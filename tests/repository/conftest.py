from typing import Any, Dict, List

import pytest
from faker import Faker

faker_data = Faker(locale="en_US")  # TODO: constant


@pytest.fixture
def get_random_room_dicts() -> List[Dict[str, Any]]:
    random_room_dicts = []
    for _ in range(5):
        temp_room = dict(
            code=faker_data.uuid4(),
            size=faker_data.random_number(digits=3),
            price=faker_data.random_number(digits=3),
            longitude=faker_data.longitude(),
            latitude=faker_data.latitude(),
        )
        random_room_dicts.append(temp_room)
    return random_room_dicts
