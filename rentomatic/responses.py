from typing import Any


class RensponseSuccess:
    def __init__(self, value: Any = None) -> None:
        self.value = value

    def __bool__(self) -> bool:
        return True
