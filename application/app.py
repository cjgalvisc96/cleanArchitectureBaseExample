from flask import Flask

from application.rest import room


def create_app(config_name: str) -> Flask:
    app = Flask(__name__)
    config_module = f"application.config.{config_name.capitalize()}Config"
    app.config.from_object(obj=config_module)
    app.register_blueprint(blueprint=room.blueprint)
    return app
