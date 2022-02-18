from unittest import mock

from rentomatic.use_cases.room_list import room_list_use_case


def test_room_list_without_parameters(get_random_domain_rooms):
    repo = mock.Mock()
    repo.list.return_value = get_random_domain_rooms
    result = room_list_use_case(repo=repo)
    repo.list.asser_called_with()
    assert result == get_random_domain_rooms
