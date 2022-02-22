from typing import Any, Dict, List

from rentomatic.domain.room import Room


class MemRepo:
    def __init__(self, *, data: List[Dict]) -> None:
        self.data = data

    def list(self, *, filters: Any) -> List[Room]:
        rooms = []
        for room in self.data:
            rooms.append(Room.from_dict(_dict=room))
        return rooms
