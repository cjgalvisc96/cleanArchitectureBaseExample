import json
from typing import Dict

from rentomatic.domain.room import Room


class RoomJsonEncoder(json.JSONEncoder):
    def default(self, room: Room) -> Dict:
        try:
            to_serialize = {
                "code": str(room.code),
                "size": room.size,
                "price": room.price,
                "longitude": room.longitude,
                "latitude": room.latitude,
            }
            return to_serialize
        except AttributeError:
            return super().default(room)
