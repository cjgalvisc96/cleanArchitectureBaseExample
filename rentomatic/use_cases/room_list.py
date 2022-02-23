from typing import Any, Union

from rentomatic.repository.memrepo import MemRepo
from rentomatic.responses import (
    RensponseSuccess,
    ResponseFailure,
    ResponseTypes,
    build_response_failure_from_invalid_request,
)


def room_list_use_case(
    *, repo: MemRepo, request: Any
) -> Union[RensponseSuccess, ResponseFailure]:
    if not request:
        return build_response_failure_from_invalid_request(
            invalid_request=request
        )
    try:
        rooms = repo.list(filters=request.filters)
        return RensponseSuccess(value=rooms)
    except Exception as error:
        return ResponseFailure(_type=ResponseTypes.SYSTEM_ERROR, message=error)
