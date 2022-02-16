import json

from faker import Faker

from rentomatic.serializers.room import RoomJsonEncoder

faker_data = Faker(locale="en_US")  # TODO: constant


def test_room_model_int():
    expected_code = faker_data.uuid4()
    excepted_size = faker_data.random_number(digits=3)
    excepted_price = faker_data.random_number(digits=3)
    excepted_longitude = float(faker_data.longitude())
    excepted_latitude = float(faker_data.latitude())

    room = dict(
        code=expected_code,
        size=excepted_size,
        price=excepted_price,
        longitude=excepted_longitude,
        latitude=excepted_latitude,
    )
    expected_json = f"""
        {{
            "code": "{expected_code}",
            "size": {excepted_size},
            "price": {excepted_price},
            "longitude": {excepted_longitude},
            "latitude": {excepted_latitude}
        }}
    """
    json_room = json.dumps(obj=room, cls=RoomJsonEncoder)
    assert json.loads(json_room) == json.loads(expected_json)
