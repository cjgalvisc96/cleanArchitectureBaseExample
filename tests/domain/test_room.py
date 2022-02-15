from faker import Faker

from rentomatic.domain.room import Room

faker_data = Faker(locale="en_US")


def test_room_model_int():
    expected_code = faker_data.uuid4()
    room = Room(
        code=expected_code,
        size=faker_data.random_number(digits=3),
        price=faker_data.random_number(digits=3),
        longitude=faker_data.longitude(),
        latitude=faker_data.latitude(),
    )
    assert room.code == expected_code
