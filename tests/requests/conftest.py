from typing import Tuple


def get_filters_keys() -> Tuple[str]:
    filters_keys = (
        "code__eq",
        "price__eq",
        "price__lt",
        "price__gt",
    )
    return filters_keys
