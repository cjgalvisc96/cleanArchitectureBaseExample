import pytest
from faker import Faker

from rentomatic.requests.room_list import build_room_list_request
from tests.requests.conftest import get_filters_keys

faker_data = Faker(locale="en_US")  # TODO: constant


def test_build_room_list_request_without_parameters():
    request = build_room_list_request()
    assert request.filters is None
    assert bool(request) is True


def test_build_room_list_request_with_empty_filters():
    request = build_room_list_request(filters={})
    assert request.filters == {}
    assert bool(request) is True


def test_build_room_list_request_with_invalid_filters_parameter():
    invalid_filter = faker_data.random_number(digits=1)
    request = build_room_list_request(filters=invalid_filter)
    assert request.has_errors()
    assert request.errors[0]["parameter"] == "filters"
    assert bool(request) is False


def test_build_room_list_request_with_incorrect_filter_keys():
    invalid_filter = {
        f"{faker_data.random_lowercase_letter()}": faker_data.random_number(
            digits=1
        )
    }
    request = build_room_list_request(filters=invalid_filter)
    assert request.has_errors()
    assert request.errors[0]["parameter"] == "filters"
    assert bool(request) is False


@pytest.mark.parametrize("key", get_filters_keys())
def test_build_room_list_request_accepted_filters(key):
    filters = {key: 1}
    request = build_room_list_request(filters=filters)
    assert request.filters == filters
    assert bool(request) is True


@pytest.mark.parametrize("key", ("code__lt", "code__gt"))
def test_build_room_list_request_rejected_filters(key):
    filters = {key: 1}
    request = build_room_list_request(filters=filters)
    assert request.has_errors()
    assert request.errors[0]["parameter"] == "filters"
    assert bool(request) is False
