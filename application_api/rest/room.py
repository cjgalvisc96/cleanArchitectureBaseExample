import json
from typing import Dict, Generator, List

from faker import Faker
from flask import Blueprint, Response, request

from application_api.rest.constants import RESPONSE_STATUS_CODES
from rentomatic.repository.memrepo import MemRepo
from rentomatic.requests.room_list import build_room_list_request
from rentomatic.serializers.room import RoomJsonEncoder
from rentomatic.use_cases.room_list import room_list_use_case

blueprint = Blueprint("room", __name__)


def build_random_rooms() -> List[Dict]:
    faker_data = Faker(locale="en_US")  # TODO: constant
    random_rooms = []
    for _ in range(5):
        temp_room = dict(
            code=faker_data.uuid4(),
            size=faker_data.random_number(digits=3),
            price=faker_data.random_number(digits=3),
            longitude=faker_data.longitude(),
            latitude=faker_data.latitude(),
        )
        random_rooms.append(temp_room)
    return random_rooms


rooms = build_random_rooms()


@blueprint.route("/rooms", methods=["GET"])
def room_list() -> Response:
    query_params = request.args.items()
    filters = get_filters_from_query_params(query_params=query_params)

    request_object = build_room_list_request(filters=filters)

    repo = MemRepo(data=rooms)
    response = room_list_use_case(repo=repo, request=request_object)
    return Response(
        response=json.dumps(obj=response.value, cls=RoomJsonEncoder),
        mimetype="application/json",  # TODO: make env var
        status=RESPONSE_STATUS_CODES[response.type],
    )


def get_filters_from_query_params(query_params: Generator) -> Dict[str, str]:
    filters = {}
    filter_prefix = "filter_"
    for arg, values in query_params:
        if arg.startswith(filter_prefix):
            filters[arg.replace(filter_prefix, "")] = values

    return filters
