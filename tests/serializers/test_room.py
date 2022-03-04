import json

from rentomatic.serializers.room import RoomJsonEncoder
from tests.utils.faker_data import faker_data


def test_room_model_init():
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
