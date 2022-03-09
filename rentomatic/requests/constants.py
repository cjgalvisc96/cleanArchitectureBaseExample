from typing import Tuple


class RequestFiltersType:
    CODE__EQ = "code__eq"
    PRICE__EQ = "price__eq"
    PRICE__LT = "price__lt"
    PRICE__GT = "price__gt"

    @classmethod
    def get_request_filters(cls) -> Tuple[str]:
        request_filters = (
            cls.CODE__EQ,
            cls.PRICE__EQ,
            cls.PRICE__LT,
            cls.PRICE__GT,
        )
        return request_filters
