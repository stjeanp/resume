"""
Global stuff like fixtures and helpers live here
"""

import pytest

from resume_app import create_app


@pytest.fixture(name="test_config_data")
def fixture_test_config_data() -> tuple[dict, dict]:
    """
    A fully functional set of config values for app testing.
    """
    config_data = {
        "BIND_ADDRS": "127.0.0.1,[::1],testing",
        "BIND_PORT": "9000",
        "DATA_PATH": "tests/test_data/resume.json",
        "LOG_LEVEL": "DEBUG",
        "SECRET_KEY": "testing",
    }
    expected_config_data = {
        "BIND_ADDRS": ["127.0.0.1", "[::1]", "testing"],
        "BIND_PORT": 9000,
        "DATA_PATH": "tests/test_data/resume.json",
        "LOG_LEVEL": "DEBUG",
        "SECRET_KEY": "testing",
    }
    return (config_data, expected_config_data)
