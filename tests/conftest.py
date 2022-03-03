import pytest

from application_api.app import create_app
from manage import read_json_configuration


@pytest.fixture
def app():
    app = create_app(
        config_name="testing"
    )  # TODO: convert this in environment var
    return app


def pytest_addoption(parser):
    parser.addoption(
        "--integration", action="store_true", help="run integration tests"
    )


def pytest_runtest_setup(item):
    if "integration" in item.keywords and not item.config.getvalue(
        "integration"
    ):
        pytest.skip("need --integration option to run")


@pytest.fixture(scope="session")
def app_configuration():
    return read_json_configuration(config="testing")  # TODO: make env
