import dataclasses
import uuid
from typing import Any, Dict


@dataclasses.dataclass
class Room:
    code: uuid.UUID
    size: int
    price: int
    longitude: float
    latitude: float

    @classmethod
    def from_dict(cls, *, _dict: Dict) -> Any:
        return cls(**_dict)

    def to_dict(self) -> Dict:
        return dataclasses.asdict(self)
