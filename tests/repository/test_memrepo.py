from operator import itemgetter
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


def get_rooms_ordered_by_field(
    *, field: str, room_dicts: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    rooms_ordered = {}
    rooms_ordered = sorted(room_dicts, key=itemgetter(field))
    return rooms_ordered


random_room_dicts = get_random_room_dicts()
rooms_order_by_size = get_rooms_ordered_by_field(
    field="size", room_dicts=random_room_dicts
)
rooms_order_by_price = get_rooms_ordered_by_field(
    field="price", room_dicts=random_room_dicts
)
rooms_order_by_longitude = get_rooms_ordered_by_field(
    field="longitude", room_dicts=random_room_dicts
)
rooms_order_by_latitude = get_rooms_ordered_by_field(
    field="latitude", room_dicts=random_room_dicts
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
        rooms_order_by_price[1]["price"] + CLEARANCE,
        str(rooms_order_by_price[1]["price"] + CLEARANCE),
    ],
)
def test_repository_list_with_price_less_than_filter(price):
    repo = MemRepo(data=random_room_dicts)
    rooms = repo.list(filters={"price__lt": price})

    excepted_len_of_rooms = 2
    assert len(rooms) == excepted_len_of_rooms

    excepted_rooms = get_rooms_ordered_by_field(
        field="price",
        room_dicts=[room.to_dict() for room in rooms],
    )
    for index_room, room in enumerate(
        rooms_order_by_price[:excepted_len_of_rooms]
    ):
        assert room["code"] == excepted_rooms[index_room]["code"]
        assert room["price"] == int(excepted_rooms[index_room]["price"])


@pytest.mark.parametrize(
    argnames="price",
    argvalues=[
        rooms_order_by_price[-2]["price"] - CLEARANCE,
        str(rooms_order_by_price[-2]["price"] - CLEARANCE),
    ],
)
def test_repository_list_with_price_greater_than_filter(price):
    repo = MemRepo(data=random_room_dicts)
    rooms = repo.list(filters={"price__gt": price})

    excepted_len_of_rooms = 2
    assert len(rooms) == excepted_len_of_rooms

    excepted_rooms = get_rooms_ordered_by_field(
        field="price",
        room_dicts=[room.to_dict() for room in rooms],
    )
    for index_room, room in enumerate(
        rooms_order_by_price[-excepted_len_of_rooms:]
    ):
        assert room["code"] == excepted_rooms[index_room]["code"]
        assert room["price"] == int(excepted_rooms[index_room]["price"])


def test_repository_list_with_price_between_filter():
    repo = MemRepo(data=random_room_dicts)
    less_price = rooms_order_by_price[0]["price"]
    greater_price = rooms_order_by_price[2]["price"]
    rooms = repo.list(
        filters={"price__lt": greater_price, "price__gt": less_price}
    )

    assert len(rooms) == 1
    rooms_order_by_price[1]["code"] == rooms[0].code
    rooms_order_by_price[1]["price"] == rooms[0].price
