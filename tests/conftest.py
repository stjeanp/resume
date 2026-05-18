"""
Global stuff like fixtures and helpers live here
"""

import pytest

from resume_app import create_app


@pytest.fixture(name="test_config_data")
def fixture_test_config_data() -> tuple[dict, dict]:
    """
    A fully functional set of config values, along with the post-processed
    expected values, for app testing.
    """
    config_data = {
        "APPLICATION_ROOT": "/",
        "BIND_ADDRS": "127.0.0.1,[::1],testing",
        "BIND_PORT": "9000",
        "DATA_PATH": "data/resume.json",
        "LOG_LEVEL": "DEBUG",
        "PREFERRED_URL_SCHEME": "http",
        "SECRET_KEY": "testing",
        "SERVER_NAME": "localhost",
    }
    expected_config_data = {
        "APPLICATION_ROOT": "/",
        "BIND_ADDRS": ["127.0.0.1", "[::1]", "testing"],
        "BIND_PORT": 9000,
        "DATA_PATH": "data/resume.json",
        "LOG_LEVEL": "DEBUG",
        "PREFERRED_URL_SCHEME": "http",
        "SECRET_KEY": "testing",
        "SERVER_NAME": "localhost",
    }
    return (config_data, expected_config_data)


@pytest.fixture(name="app")
def fixture_app(test_config_data):
    """
    Fixture to return the current Flask app's application context
    """
    config_data, _expected_data = test_config_data
    config_data["TESTING"] = True
    app = create_app(config_data)
    with app.app_context():
        yield app


@pytest.fixture(name="client")
def fixture_client(app):
    """
    Fixture to return the current application context's test_client()
    """
    return app.test_client()
