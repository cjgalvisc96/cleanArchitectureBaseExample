import pytest

from config.config import settings
from rentomatic.repository.postgres.postgresrepo import PostgresRepo
from tests.utils.utils import get_rooms_ordered_by_field

pytestmark = pytest.mark.integration

CLEARANCE = 1
postgres_repo_configuration = dict(POSTGRES_URI=settings.POSTGRES_URI)


def test_repository_list_without_parameters(
    postgres_session, postgres_test_data
):
    repo = PostgresRepo(configuration=postgres_repo_configuration)
    repo_rooms = repo.list()
    assert set([room.code for room in repo_rooms]) == set(
        [room["code"] for room in postgres_test_data]
    )


def test_repository_list_with_code_equals_filter(
    postgres_session, postgres_test_data
):
    repo = PostgresRepo(configuration=postgres_repo_configuration)
    index_expected_room = 0
    excepted_room_code = postgres_test_data[index_expected_room]["code"]
    rooms = repo.list(filters={"code__eq": excepted_room_code})
    excepted_len_of_rooms = 1
    assert len(rooms) == excepted_len_of_rooms
    assert rooms[index_expected_room].code == excepted_room_code


def test_repository_list_with_price_equals_filter(
    postgres_session, postgres_test_data
):
    repo = PostgresRepo(configuration=postgres_repo_configuration)
    index_expected_room = 0
    prices_to_test = (
        postgres_test_data[index_expected_room]["price"],
        str(postgres_test_data[index_expected_room]["price"]),
    )
    for price_to_test in prices_to_test:
        rooms = repo.list(filters={"price__eq": price_to_test})
        excepted_len_of_rooms = 1
        assert len(rooms) == excepted_len_of_rooms
        assert (
            rooms[index_expected_room].code
            == postgres_test_data[index_expected_room]["code"]
        )
        assert rooms[index_expected_room].price == int(price_to_test)


def test_repository_list_with_price_less_than_filter(
    postgres_session, postgres_test_data
):
    repo = PostgresRepo(configuration=postgres_repo_configuration)
    rooms_order_by_price = get_rooms_ordered_by_field(
        field="price", room_dicts=postgres_test_data
    )
    index_expected_room = 1
    price_to_test = (
        rooms_order_by_price[index_expected_room]["price"] + CLEARANCE
    )

    rooms = repo.list(filters={"price__lt": price_to_test})

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


def test_repository_list_with_price_greater_than_filter(
    postgres_session, postgres_test_data
):
    repo = PostgresRepo(configuration=postgres_repo_configuration)
    rooms_order_by_price = get_rooms_ordered_by_field(
        field="price", room_dicts=postgres_test_data
    )
    index_expected_room = -2
    price_to_test = (
        rooms_order_by_price[index_expected_room]["price"] - CLEARANCE
    )

    rooms = repo.list(filters={"price__gt": price_to_test})

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


def test_repository_list_with_price_between_filter(
    postgres_session, postgres_test_data
):
    repo = PostgresRepo(configuration=postgres_repo_configuration)
    rooms_order_by_price = get_rooms_ordered_by_field(
        field="price", room_dicts=postgres_test_data
    )
    index_expected_less_price = 0
    index_expected_greater_price = 2
    less_price = rooms_order_by_price[index_expected_less_price]["price"]
    greater_price = rooms_order_by_price[index_expected_greater_price]["price"]
    rooms = repo.list(
        filters={"price__lt": greater_price, "price__gt": less_price}
    )

    excepted_len_of_rooms = 1
    assert len(rooms) == excepted_len_of_rooms

    index_expected_room = 1
    room = rooms[0]
    assert room.code == rooms_order_by_price[index_expected_room]["code"]
    assert room.price == rooms_order_by_price[index_expected_room]["price"]
