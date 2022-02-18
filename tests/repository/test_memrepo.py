from rentomatic.domain.room import Room
from rentomatic.repository.memrepo import MemRepo


def test_repository_list_without_parameters(get_random_room_dicts):
    repo = MemRepo(data=get_random_room_dicts)
    rooms = [Room.from_dict(_dict=room) for room in get_random_room_dicts]
    assert repo.list() == rooms
