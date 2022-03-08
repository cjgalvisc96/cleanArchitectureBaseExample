from operator import itemgetter
from typing import Any, Dict, List

from faker import Faker

from config.config import settings
from rentomatic.domain.room import Room

faker_data = Faker(locale=settings.FAKER_DATA_LOCATE)


def get_rooms_ordered_by_field(
    *, field: str, room_dicts: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    rooms_ordered = {}
    rooms_ordered = sorted(room_dicts, key=itemgetter(field))
    return rooms_ordered


def get_random_room_dicts() -> List[Dict[str, Any]]:
    random_room_dicts = []
    for _ in range(settings.NUMBER_OF_RANDOM_TEST_ROOMS):
        temp_room = dict(
            code=faker_data.uuid4(),
            size=faker_data.random_number(digits=3),
            price=faker_data.random_number(digits=3),
            longitude=float(faker_data.longitude()),
            latitude=float(faker_data.latitude()),
        )
        random_room_dicts.append(temp_room)
    return random_room_dicts


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
