from typing import Any, Dict, List

from rentomatic.domain.room import Room
from rentomatic.repository.constants import FiltersType


class MemRepo:
    def __init__(self, *, data: List[Dict]) -> None:
        self.data = data

    def list(self, *, filters: Any = None) -> List[Room]:
        result = []
        result = [Room.from_dict(_dict=room) for room in self.data]

        if not filters:
            return result

        if FiltersType.CODE__EQ in filters:
            result = [
                room
                for room in result
                if room.code == filters[FiltersType.CODE__EQ]
            ]

        if FiltersType.PRICE__EQ in filters:
            result = [
                room
                for room in result
                if room.price == int(filters[FiltersType.PRICE__EQ])
            ]

        if FiltersType.PRICE__LT in filters:
            result = [
                room
                for room in result
                if room.price < int(filters[FiltersType.PRICE__LT])
            ]

        if FiltersType.PRICE__GT in filters:
            result = [
                room
                for room in result
                if room.price > int(filters[FiltersType.PRICE__GT])
            ]

        return result
