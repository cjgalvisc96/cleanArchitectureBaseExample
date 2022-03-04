import pytest

from rentomatic.requests.room_list import build_room_list_request
from tests.requests.conftest import get_filters_names
from tests.utils.faker_data import faker_data


def test_build_room_list_request_without_parameters():
    request = build_room_list_request(filters=None)
    assert request.filters is None
    assert bool(request) is True


def test_build_room_list_request_with_empty_filters():
    request = build_room_list_request(filters={})
    assert request.filters == {}
    assert bool(request) is True


def test_build_room_list_request_with_invalid_filters_parameter():
    invalid_filter = faker_data.random_digit()
    request = build_room_list_request(filters=invalid_filter)
    assert request.has_errors()
    assert request.errors[0]["parameter"] == "filters"
    assert request.errors[0]["message"] == "Is not iterable"
    assert bool(request) is False


def test_build_room_list_request_with_incorrect_filter_names():
    invalid_filter_name = faker_data.random_lowercase_letter()
    invalid_filter = {f"{invalid_filter_name}": faker_data.random_digit()}
    request = build_room_list_request(filters=invalid_filter)
    assert request.has_errors()
    assert request.errors[0]["parameter"] == "filters"
    assert (
        request.errors[0]["message"]
        == f"Filter with name {invalid_filter_name} cannot be used"
    )
    assert bool(request) is False


@pytest.mark.parametrize("filter_name", get_filters_names())
def test_build_room_list_request_accepted_filters(filter_name):
    filters = {filter_name: 1}
    request = build_room_list_request(filters=filters)
    assert request.filters == filters
    assert bool(request) is True


@pytest.mark.parametrize("filter_name", ("code__lt", "code__gt"))
def test_build_room_list_request_rejected_filters(filter_name):
    filters = {filter_name: 1}
    request = build_room_list_request(filters=filters)
    assert request.has_errors()
    assert request.errors[0]["parameter"] == "filters"
    assert (
        request.errors[0]["message"]
        == f"Filter with name {filter_name} cannot be used"
    )
    assert bool(request) is False
