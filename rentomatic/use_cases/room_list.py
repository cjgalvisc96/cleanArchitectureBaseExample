from typing import Any, List

from rentomatic.domain.room import Room


def room_list_use_case(*, repo: Any) -> List[Room]:
    return repo.list()
