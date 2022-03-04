from rentomatic.domain.room import Room
from tests.utils.faker_data import faker_data


def test_room_model_init():
    expected_code = faker_data.uuid4()
    excepted_size = faker_data.random_number(digits=3)
    excepted_price = faker_data.random_number(digits=3)
    excepted_longitude = faker_data.longitude()
    excepted_latitude = faker_data.latitude()

    room = Room(
        code=expected_code,
        size=excepted_size,
        price=excepted_price,
        longitude=excepted_longitude,
        latitude=excepted_latitude,
    )
    assert room.code == expected_code
    assert room.size == excepted_size
    assert room.price == excepted_price
    assert room.longitude == excepted_longitude
    assert room.latitude == excepted_latitude


def test_room_model_from_dict():
    expected_code = faker_data.uuid4()
    excepted_size = faker_data.random_number(digits=3)
    excepted_price = faker_data.random_number(digits=3)
    excepted_longitude = faker_data.longitude()
    excepted_latitude = faker_data.latitude()

    init_dict = dict(
        code=expected_code,
        size=excepted_size,
        price=excepted_price,
        longitude=excepted_longitude,
        latitude=excepted_latitude,
    )
    room = Room.from_dict(_dict=init_dict)
    assert room.code == expected_code
    assert room.size == excepted_size
    assert room.price == excepted_price
    assert room.longitude == excepted_longitude
    assert room.latitude == excepted_latitude


def test_room_model_to_dict():
    init_dict = dict(
        code=faker_data.uuid4(),
        size=faker_data.random_number(digits=3),
        price=faker_data.random_number(digits=3),
        longitude=faker_data.longitude(),
        latitude=faker_data.latitude(),
    )
    room = Room.from_dict(_dict=init_dict)
    assert room.to_dict() == init_dict


def test_room_model_comparasion():
    init_dict = dict(
        code=faker_data.uuid4(),
        size=faker_data.random_number(digits=3),
        price=faker_data.random_number(digits=3),
        longitude=faker_data.longitude(),
        latitude=faker_data.latitude(),
    )
    room_1 = Room.from_dict(_dict=init_dict)
    room_2 = Room.from_dict(_dict=init_dict)
    assert room_1 == room_2
