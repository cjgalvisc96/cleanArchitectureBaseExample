from typing import Any, Dict, List, Optional

from pymongo import MongoClient
from pymongo.cursor import Cursor

from config.config import settings
from rentomatic.domain.room import Room


class MongoRepo:
    def __init__(self) -> None:
        client = MongoClient(settings.MONGODB_URI)
        self.db = client[settings.APPLICATION_DB]

    def _create_room_objects(self, *, results: Cursor) -> List[Room]:
        room_objects = [
            Room(
                code=result["code"],
                size=result["size"],
                price=result["price"],
                latitude=result["latitude"],
                longitude=result["longitude"],
            )
            for result in results
        ]
        return room_objects

    def list(self, *, filters=Optional[Dict[str, Any]]) -> List[Room]:
        def build_mongo_filters() -> Dict[str, Dict[str, Any]]:
            mongo_filter = {}
            for key, value in filters.items():
                key, operator = key.split("__")
                filter_value = mongo_filter.get(key, {})
                if key == "price":
                    value = int(value)

                filter_value["${}".format(operator)] = value
                mongo_filter[key] = filter_value
            return mongo_filter

        collection = self.db.rooms

        if filters is None or not isinstance(filters, dict):
            result = collection.find()
            return self._create_room_objects(results=result)

        mongo_filters = build_mongo_filters()
        result = collection.find(mongo_filters)
        return self._create_room_objects(results=result)
