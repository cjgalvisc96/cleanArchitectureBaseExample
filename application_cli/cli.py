from flask import request

from rentomatic.repository.memrepo import MemRepo
from rentomatic.requests.room_list import build_room_list_request
from rentomatic.use_cases.room_list import room_list_use_case
from tests.utils.utils import get_random_room_dicts

rooms = get_random_room_dicts()

if __name__ == "__main__":
    request = build_room_list_request(filters=None)
    repo = MemRepo(data=rooms)
    result = room_list_use_case(repo=repo, request=request)
    print([room.to_dict() for room in result.value])
