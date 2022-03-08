from typing import Dict


def get_status_codes() -> Dict[str, int]:
    expected_status_codes = dict(
        HTTP_200_OK=200,
        HTTP_400_BAD_REQUEST=400,
        HTTP_404_NOT_FOUND=404,
        HTTP_500_INTERNAL_SERVER_ERROR=500,
    )
    return expected_status_codes
