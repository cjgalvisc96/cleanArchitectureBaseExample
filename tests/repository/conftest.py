from typing import Dict, List

import pytest
from faker import Faker

faker_data = Faker(locale="en_US")  # TODO: constant


@pytest.fixture
def room_dicts() -> List[Dict]:
    rooms = [
        {
            "code": faker_data.uuid4(),
            "size": faker_data.random_number(digits=3),
            "price": faker_data.random_number(digits=3),
            "longitude": faker_data.longitude(),
            "latitude": faker_data.latitude(),
        },
        {
            "code": faker_data.uuid4(),
            "size": faker_data.random_number(digits=3),
            "price": faker_data.random_number(digits=3),
            "longitude": faker_data.longitude(),
            "latitude": faker_data.latitude(),
        },
        {
            "code": faker_data.uuid4(),
            "size": faker_data.random_number(digits=3),
            "price": faker_data.random_number(digits=3),
            "longitude": faker_data.longitude(),
            "latitude": faker_data.latitude(),
        },
        {
            "code": faker_data.uuid4(),
            "size": faker_data.random_number(digits=3),
            "price": faker_data.random_number(digits=3),
            "longitude": faker_data.longitude(),
            "latitude": faker_data.latitude(),
        },
    ]
    return rooms
