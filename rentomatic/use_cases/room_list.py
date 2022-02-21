from typing import Any

from rentomatic.responses import RensponseSuccess


def room_list_use_case(*, repo: Any, request: Any) -> RensponseSuccess:
    rooms = repo.list()
    return RensponseSuccess(value=rooms)
