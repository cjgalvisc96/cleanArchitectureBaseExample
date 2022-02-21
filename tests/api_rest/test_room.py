import json
from unittest import mock

from tests.api_rest.conftest import get_status_codes

STATUS_CODES = get_status_codes()


@mock.patch("application_api.rest.room.room_list_use_case")
def test_get_rooms(mock_list_use_case, get_random_rooms, client):
    rooms = get_random_rooms
    mock_list_use_case.return_value = rooms
    http_response = client.get("/rooms")

    expected_rooms = [room.to_dict() for room in rooms]
    assert (
        json.loads(http_response.data.decode("UTF-8")) == expected_rooms
    )  # TODO: environment var

    mock_list_use_case.assert_called()
    assert http_response.status_code == STATUS_CODES["HTTP_200_OK"]
    assert http_response.mimetype == "application/json"
