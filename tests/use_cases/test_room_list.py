from unittest import mock

from rentomatic.requests.room_list import build_room_list_request
from rentomatic.responses import ResponseTypes
from rentomatic.use_cases.room_list import room_list_use_case
from tests.utils.utils import faker_data


def test_room_list_without_parameters(get_random_domain_rooms):
    repo = mock.Mock()
    repo.list.return_value = get_random_domain_rooms
    request = build_room_list_request(filters=None)
    response = room_list_use_case(repo=repo, request=request)

    assert bool(response) is True
    repo.list.asser_called_with(filters=None)
    assert response.value == get_random_domain_rooms


def test_room_list_with_filters(get_random_domain_rooms):
    repo = mock.Mock()
    random_domain_rooms = get_random_domain_rooms
    repo.list.return_value = random_domain_rooms
    expected_filters = {"code__eq": random_domain_rooms[0].code}
    request = build_room_list_request(filters=expected_filters)
    response = room_list_use_case(repo=repo, request=request)

    assert bool(response) is True
    repo.list.asser_called_with(filters=expected_filters)
    assert response.value == random_domain_rooms


def test_room_list_handles_generic_error():
    repo = mock.Mock()
    expected_exception_error_message = "Just an error message"
    repo.list.side_effect = Exception(expected_exception_error_message)

    request = build_room_list_request(filters={})
    response = room_list_use_case(repo=repo, request=request)

    assert bool(response) is False
    repo.list.asser_called_with(filters={})
    assert response.value == {
        "type": ResponseTypes.SYSTEM_ERROR,
        "message": f"Exception: {expected_exception_error_message}",
    }


def test_room_list_handles_bad_request():
    repo = mock.Mock()
    expected_invalid_filter = faker_data.random_digit()

    request = build_room_list_request(filters=expected_invalid_filter)
    response = room_list_use_case(repo=repo, request=request)

    assert bool(response) is False
    repo.list.asser_called_with(filters=expected_invalid_filter)
    expected_error_message = "filters: Is not iterable\n"
    assert response.value == {
        "type": ResponseTypes.PARAMETERS_ERROR,
        "message": expected_error_message,
    }
