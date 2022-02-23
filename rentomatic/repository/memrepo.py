from typing import Any, Dict, List

from rentomatic.domain.room import Room


class MemRepo:
    def __init__(self, *, data: List[Dict]) -> None:
        self.data = data

    def list(self, *, filters: Any = None) -> List[Room]:
        rooms = [Room.from_dict(_dict=room) for room in self.data]

        if not filters:
            return rooms

        return rooms
