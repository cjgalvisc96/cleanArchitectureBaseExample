import pytest

from application_api.app import create_app


@pytest.fixture
def app():
    app = create_app("testing")  # TODO: convert this in environment var
    return app
