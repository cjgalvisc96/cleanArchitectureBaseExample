import pytest

from application_api.app import create_app


@pytest.fixture
def app():
    app = create_app(config_name="testing")
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
