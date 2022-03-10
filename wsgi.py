from application_api.app import create_app
from config.config import settings

app = create_app(config_name=settings.FLASK_CONFIG)
