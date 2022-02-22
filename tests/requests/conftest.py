from typing import Tuple


def get_filters_names() -> Tuple[str]:
    filters_names = (
        "code__eq",
        "price__eq",
        "price__lt",
        "price__gt",
    )
    return filters_names
