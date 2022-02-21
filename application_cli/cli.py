from typing import Dict, List

from faker import Faker

from rentomatic.repository.memrepo import MemRepo
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
    repo = MemRepo(data=rooms)
    result = room_list_use_case(repo=repo)
    print([room.to_dict() for room in result])
