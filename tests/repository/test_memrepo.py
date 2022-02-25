from typing import Any, Dict, List

import pytest
from faker import Faker

from rentomatic.domain.room import Room
from rentomatic.repository.memrepo import MemRepo

faker_data = Faker(locale="en_US")  # TODO: constant

CLEARANCE = 1


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


def get_min_and_max_fields_in_room_dicts(
    *, room_dicts: List[Dict[str, Any]]
) -> Dict[str, Dict[str, int]]:
    """return:
    min_and_max_fields = {
        "example_field": {
            "min": 1,
            "max": 100,
        }...
    }
    """
    min_and_max_fields = {}
    fields = room_dicts[0].keys()
    for field in fields:
        min_room_by_field = min(random_room_dicts, key=lambda x: x[field])
        max_room_by_field = max(random_room_dicts, key=lambda x: x[field])
        min_and_max_fields[field] = {
            "min": min_room_by_field[field],
            "max": max_room_by_field[field],
        }
    return min_and_max_fields


def find_room_in_rooms_by_field_and_field_value(
    *, rooms: List[Dict], field: str, field_value: Any
) -> Dict:
    find_room = next(
        (room for room in rooms if room[field] == field_value), {}
    )
    return find_room


random_room_dicts = get_random_room_dicts()
min_and_max_fields = get_min_and_max_fields_in_room_dicts(
    room_dicts=random_room_dicts
)


def test_repository_list_without_parameters():
    repo = MemRepo(data=random_room_dicts)
    rooms = [Room.from_dict(_dict=room) for room in random_room_dicts]
    assert repo.list(filters=None) == rooms


def test_repository_list_with_code_equals_filter():
    repo = MemRepo(data=random_room_dicts)
    excepted_room_code = random_room_dicts[0]["code"]
    rooms = repo.list(filters={"code__eq": excepted_room_code})
    assert len(rooms) == 1
    assert rooms[0].code == excepted_room_code


@pytest.mark.parametrize(
    argnames="price",
    argvalues=[
        random_room_dicts[0]["price"],
        str(random_room_dicts[0]["price"]),
    ],
)
def test_repository_list_with_price_equals_filter(price):
    repo = MemRepo(data=random_room_dicts)
    excepted_room_code = random_room_dicts[0]["code"]
    rooms = repo.list(filters={"price__eq": price})
    assert len(rooms) == 1
    assert rooms[0].code == excepted_room_code
    assert rooms[0].price == int(price)


@pytest.mark.parametrize(
    argnames="price",
    argvalues=[
        min_and_max_fields["price"]["min"] + CLEARANCE,
        str(min_and_max_fields["price"]["min"] + CLEARANCE),
    ],
)
def test_repository_list_with_price_less_than_filter(price):
    repo = MemRepo(data=random_room_dicts)
    expected_room = find_room_in_rooms_by_field_and_field_value(
        rooms=random_room_dicts,
        field="price",
        field_value=min_and_max_fields["price"]["min"],
    )
    rooms = repo.list(filters={"price__lt": price})
    assert len(rooms) == 1
    assert rooms[0].code == expected_room["code"]
    assert rooms[0].price == int(expected_room["price"])
