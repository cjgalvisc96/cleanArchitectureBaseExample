from typing import Dict, List

from faker import Faker
from flask import request

from rentomatic.repository.memrepo import MemRepo
from rentomatic.requests.room_list import build_room_list_request
from rentomatic.use_cases.room_list import room_list_use_case


def build_random_rooms() -> List[Dict]:
    faker_data = Faker(locale="en_US")  # TODO: constant
    random_rooms = []
    for _ in range(5):
        temp_room = dict(
            code=faker_data.uuid4(),
            size=faker_data.random_number(digits=3),
            price=faker_data.random_number(digits=3),
            longitude=faker_data.longitude(),
            latitude=faker_data.latitude(),
        )
        random_rooms.append(temp_room)
    return random_rooms


rooms = build_random_rooms()

if __name__ == "__main__":
    request = build_room_list_request(filters=None)
    repo = MemRepo(data=rooms)
    result = room_list_use_case(repo=repo, request=request)
    print([room.to_dict() for room in result.value])
