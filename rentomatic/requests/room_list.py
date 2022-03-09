from collections.abc import Mapping
from typing import Union

from rentomatic.requests.constants import RequestFiltersType
from rentomatic.requests.error_messages import filters_errors


class RoomListInvalidRequest:
    def __init__(self) -> None:
        self.errors = []

    def add_error(self, *, parameter: str, message: str) -> None:
        self.errors.append({"parameter": parameter, "message": message})

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def __bool__(self) -> bool:
        return False


class RoomListValidRequest:
    def __init__(self, *, filters=None) -> None:
        self.filters = filters

    def __bool__(self) -> bool:
        return True


def build_room_list_request(
    *,
    filters=None,
) -> Union[RoomListValidRequest, RoomListInvalidRequest]:
    if filters is not None:
        error_filter_parameter = "filters"
        invalid_request = RoomListInvalidRequest()
        if not isinstance(filters, Mapping):
            invalid_request.add_error(
                parameter=error_filter_parameter,
                message=filters_errors["not_iterable"],
            )
            return invalid_request

        accepted_filters = RequestFiltersType.get_request_filters()
        for filter_name, _ in filters.items():
            if filter_name not in accepted_filters:
                invalid_request.add_error(
                    parameter=error_filter_parameter,
                    message=filters_errors["invalid_filter_name"].format(
                        filter_name=filter_name
                    ),
                )

        if invalid_request.has_errors():
            return invalid_request

    return RoomListValidRequest(filters=filters)
