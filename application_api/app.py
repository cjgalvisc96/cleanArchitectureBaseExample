from flask import Flask

from application_api.rest import room
from config.config import settings


def create_app(*, config_name: str) -> Flask:
    app = Flask(__name__)
    config_module = f"application_api.config.{config_name.capitalize()}Config"
    app.config.from_object(obj=config_module)
    app.register_blueprint(
        blueprint=room.blueprint, url_prefix=settings.API_V1_PREFIX
    )
    return app
