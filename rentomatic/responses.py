from typing import Any, Union

from rentomatic.requests.room_list import RoomListInvalidRequest


class ResponseTypes:
    PARAMETERS_ERROR = "ParametersError"
    RESOURCE_ERROR = "ResoruceError"
    SYSTEM_ERROR = "SystemError"
    SUCCESS = "Success"


class ResponseFailure:
    def __init__(self, *, _type: str, message: str) -> None:
        self.type = _type
        self.message = self.format_message(message=message)

    def format_message(self, *, message: str) -> Union[Exception, str]:
        if isinstance(message, Exception):
            return f"{message.__class__.__name__}: " f"{message}"
        return message

    @property
    def value(self):
        return {"type": self.type, "message": self.message}

    def __bool__(self):
        return False


class RensponseSuccess:
    def __init__(self, *, value: Any = None) -> None:
        self.value = value
        self.type = ResponseTypes.SUCCESS

    def __bool__(self) -> bool:
        return True


def build_response_failure_from_invalid_request(
    *, invalid_request: RoomListInvalidRequest
) -> ResponseFailure:
    message = ""
    for error in invalid_request.errors:
        message += f"{error['parameter']}: {error['message']}\n"

    return ResponseFailure(
        _type=ResponseTypes.PARAMETERS_ERROR, message=message
    )
