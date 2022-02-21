from unittest import mock

from rentomatic.requests.room_list import RoomListRequest
from rentomatic.use_cases.room_list import room_list_use_case


def test_room_list_without_parameters(get_random_domain_rooms):
    repo = mock.Mock()
    repo.list.return_value = get_random_domain_rooms
    request = RoomListRequest()
    response = room_list_use_case(repo=repo, request=request)

    assert bool(response) is True
    repo.list.asser_called_with()
    assert response.value == get_random_domain_rooms
