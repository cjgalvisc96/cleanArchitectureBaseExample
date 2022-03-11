from application_api.app import create_app
from config.config import settings

if __name__ == "__main__":
    app = create_app(config_name=settings.FLASK_CONFIG)
    app.run(debug=True, host=settings.FLASK_HOST, port=settings.FLASK_PORT)
