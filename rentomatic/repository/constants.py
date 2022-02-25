from typing import Tuple


class FiltersEnum:
    CODE__EQ = "code__eq"
    PRICE__EQ = "price__eq"
    PRICE__LT = "price__lt"
    PRICE__GT = "price__gt"

    @classmethod
    def get_avaliable_filters(cls) -> Tuple[str]:
        AVALIABLE_FITLERS = (
            cls.CODE__EQ,
            cls.PRICE__EQ,
            cls.PRICE__LT,
            cls.PRICE__GT,
        )
        return AVALIABLE_FITLERS
