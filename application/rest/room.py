import json
from typing import Dict, List

from faker import Faker
from flask import Blueprint, Response

from application.rest.constants import STATUS_CODES
from rentomatic.repository.memrepo import MemRepo
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
def room_list():
    repo = MemRepo(data=rooms)
    result = room_list_use_case(repo=repo)
    return Response(
        response=json.dumps(obj=result, cls=RoomJsonEncoder),
        mimetype="application/json",  # TODO: make env var
        status=STATUS_CODES["HTTP_200_OK"],
    )
