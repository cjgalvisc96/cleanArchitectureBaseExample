import json
import urllib
from unittest import mock

import pytest

from config.config import settings
from rentomatic.responses import (
    RensponseSuccess,
    ResponseFailure,
    ResponseTypes,
)
from tests.application_api.conftest import get_status_codes
from tests.utils.utils import faker_data, get_random_rooms

STATUS_CODES = get_status_codes()


@mock.patch("application_api.rest.room.room_list_use_case")
def test_get_rooms_without_filters(mock_list_use_case, client):
    rooms = get_random_rooms()
    mock_list_use_case.return_value = RensponseSuccess(value=rooms)
    http_response = client.get("/rooms")

    expected_rooms = [room.to_dict() for room in rooms]
    assert (
        json.loads(http_response.data.decode(settings.ENCODING_FORMAT))
        == expected_rooms
    )

    mock_list_use_case.assert_called()
    args, kwargs = mock_list_use_case.call_args
    assert kwargs["request"].filters == {}

    assert http_response.status_code == STATUS_CODES["HTTP_200_OK"]
    assert http_response.mimetype == "application/json"


@mock.patch("application_api.rest.room.room_list_use_case")
def test_get_rooms_with_filters(mock_list_use_case, client):
    rooms = get_random_rooms()
    mock_list_use_case.return_value = RensponseSuccess(value=rooms)
    filters = {"price__gt": "2", "price__lt": "6"}

    filter_prefix = "filter_"
    filters_with_prefix = {
        f"{filter_prefix}{key}": value for key, value in filters.items()
    }

    url_params = urllib.parse.urlencode(filters_with_prefix)
    http_response = client.get(f"/rooms?{url_params}")

    expected_rooms = [room.to_dict() for room in rooms]
    assert (
        json.loads(http_response.data.decode(settings.ENCODING_FORMAT))
        == expected_rooms
    )

    mock_list_use_case.assert_called()
    args, kwargs = mock_list_use_case.call_args
    assert kwargs["request"].filters == filters

    assert http_response.status_code == STATUS_CODES["HTTP_200_OK"]
    assert http_response.mimetype == "application/json"


@pytest.mark.parametrize(
    argnames="response_type, expected_status_code",
    argvalues=[
        (ResponseTypes.PARAMETERS_ERROR, STATUS_CODES["HTTP_400_BAD_REQUEST"]),
        (ResponseTypes.RESOURCE_ERROR, STATUS_CODES["HTTP_404_NOT_FOUND"]),
        (
            ResponseTypes.SYSTEM_ERROR,
            STATUS_CODES["HTTP_500_INTERNAL_SERVER_ERROR"],
        ),
    ],
)
@mock.patch("application_api.rest.room.room_list_use_case")
def test_get_response_failures(
    mock_list_use_case, client, response_type, expected_status_code
):
    expected_error_message = "Just an error message"
    mock_list_use_case.return_value = ResponseFailure(
        _type=response_type, message=expected_error_message
    )
    filters = faker_data.word()
    http_response = client.get(f"/rooms?{filters}")
    response = json.loads(http_response.data.decode(settings.ENCODING_FORMAT))

    assert response["message"] == expected_error_message

    mock_list_use_case.assert_called()
    args, kwargs = mock_list_use_case.call_args
    assert kwargs["request"].filters == {}

    assert http_response.status_code == expected_status_code
    assert http_response.mimetype == "application/json"
