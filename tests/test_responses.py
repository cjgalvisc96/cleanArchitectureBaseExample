from rentomatic.requests.room_list import RoomListInvalidRequest
from rentomatic.responses import (
    RensponseSuccess,
    ResponseFailure,
    ResponseTypes,
    build_response_failure_from_invalid_request,
)

SUCCESS_VALUE = {"key": ["value1", "value2"]}
GENERIC_REPONSE_TYPE = "Response"
GENERIC_REPONSE_MESAGGE = "This is a response"


def test_response_success_is_true():
    response = RensponseSuccess(value=SUCCESS_VALUE)
    assert bool(response) is True


def test_response_failure_is_false():
    response = ResponseFailure(
        _type=GENERIC_REPONSE_TYPE, message=GENERIC_REPONSE_MESAGGE
    )
    assert bool(response) is False


def test_response_success_has_type_and_value():
    response = RensponseSuccess(value=SUCCESS_VALUE)
    assert response.type == ResponseTypes.SUCCESS
    assert response.value == SUCCESS_VALUE


def test_response_failure_has_type_and_message():
    response = ResponseFailure(
        _type=GENERIC_REPONSE_TYPE, message=GENERIC_REPONSE_MESAGGE
    )

    assert response.type == GENERIC_REPONSE_TYPE
    assert response.message == GENERIC_REPONSE_MESAGGE
    assert response.value == {
        "type": GENERIC_REPONSE_TYPE,
        "message": GENERIC_REPONSE_MESAGGE,
    }


def test_response_failure_initialisation_with_exception():
    excepted_exception_message = "Just an error message"
    response = ResponseFailure(
        _type=GENERIC_REPONSE_TYPE,
        message=Exception(excepted_exception_message),
    )

    assert bool(response) is False
    assert response.type == GENERIC_REPONSE_TYPE
    assert response.message == f"Exception: {excepted_exception_message}"


def test_reponse_failure_from_empty_invalid_request():
    response = build_response_failure_from_invalid_request(
        invalid_request=RoomListInvalidRequest()
    )

    assert bool(response) is False
    assert response.type == ResponseTypes.PARAMETERS_ERROR


def test_response_failure_from_invalid_request_with_errors():
    request = RoomListInvalidRequest()
    excepted_error_1 = "Is mandatory"
    excepted_error_2 = "Can't be blank"
    excepted_parameter_error = "path"

    request.add_error(
        parameter=excepted_parameter_error, message=excepted_error_1
    )
    request.add_error(
        parameter=excepted_parameter_error, message=excepted_error_2
    )
    response = build_response_failure_from_invalid_request(
        invalid_request=request
    )

    assert bool(response) is False
    assert response.type == ResponseTypes.PARAMETERS_ERROR
    assert response.message == (
        f"{excepted_parameter_error}: {excepted_error_1}\n"
        f"{excepted_parameter_error}: {excepted_error_2}\n"
    )
