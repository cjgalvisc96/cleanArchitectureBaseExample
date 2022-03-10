import json
from typing import Dict, Generator

from flask import Blueprint, Response, request

from application_api.rest.constants import RESPONSE_STATUS_CODES
from config.config import settings
from rentomatic.repository.postgres.postgresrepo import PostgresRepo
from rentomatic.requests.room_list import build_room_list_request
from rentomatic.serializers.room import RoomJsonEncoder
from rentomatic.use_cases.room_list import room_list_use_case
from tests.utils.utils import get_random_room_dicts

blueprint = Blueprint("room", __name__)
rooms = get_random_room_dicts()


@blueprint.route("/rooms", methods=["GET"])
def room_list() -> Response:
    query_params = request.args.items()
    filters = get_filters_from_query_params(query_params=query_params)

    request_object = build_room_list_request(filters=filters)

    """
        ** CleanArchitecture advantage: switch beetween DB easy **
            from rentomatic.repository.memrepo import MemRepo
            repo = MemRepo(data=rooms)
    """
    repo = PostgresRepo()
    response = room_list_use_case(repo=repo, request=request_object)
    return Response(
        response=json.dumps(obj=response.value, cls=RoomJsonEncoder),
        mimetype=settings.APPLICATION_API_MIMETYPE,
        status=RESPONSE_STATUS_CODES[response.type],
    )


def get_filters_from_query_params(query_params: Generator) -> Dict[str, str]:
    filters = {}
    filter_prefix = "filter_"
    for arg, values in query_params:
        if arg.startswith(filter_prefix):
            filters[arg.replace(filter_prefix, "")] = values

    return filters
