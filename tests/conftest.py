import pytest

from application_api.app import create_app


@pytest.fixture
def app():
    app = create_app(
        config_name="testing"
    )  # TODO: convert this in environment var
    return app
