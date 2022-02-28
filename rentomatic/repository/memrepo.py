from typing import Any, Dict, List

from rentomatic.domain.room import Room
from rentomatic.repository.constants import FiltersEnum


class MemRepo:
    def __init__(self, *, data: List[Dict]) -> None:
        self.data = data

    def list(self, *, filters: Any = None) -> List[Room]:
        result = []
        result = [Room.from_dict(_dict=room) for room in self.data]

        if not filters:
            return result

        if FiltersEnum.CODE__EQ in filters:
            result = [
                room
                for room in result
                if room.code == filters[FiltersEnum.CODE__EQ]
            ]

        if FiltersEnum.PRICE__EQ in filters:
            result = [
                room
                for room in result
                if room.price == int(filters[FiltersEnum.PRICE__EQ])
            ]

        if FiltersEnum.PRICE__LT in filters:
            result = [
                room
                for room in result
                if room.price < int(filters[FiltersEnum.PRICE__LT])
            ]

        if FiltersEnum.PRICE__GT in filters:
            result = [
                room
                for room in result
                if room.price > int(filters[FiltersEnum.PRICE__GT])
            ]

        return result
