"""
Test the config parsing/validating
"""

import pytest

from resume_app.helpers.config import ResumeConfigLoader


def test_good_config(test_config_data: tuple[dict, dict]) -> None:
    """
    Test parsing and validating good config data
    """
    orig, expected = test_config_data
    config_obj = ResumeConfigLoader(orig)
    assert isinstance(config_obj, ResumeConfigLoader)
    assert isinstance(config_obj.configs, dict)
    assert config_obj.configs == expected


def test_config_getattr(test_config_data) -> None:
    """
    Test the config loader's __getattr__ method
    """
    orig, expected = test_config_data
    config_obj = ResumeConfigLoader(orig)
    assert isinstance(config_obj, ResumeConfigLoader)
    assert isinstance(config_obj.configs, dict)
    assert config_obj.configs == expected
    assert config_obj.BIND_PORT == expected["BIND_PORT"]

    with pytest.raises(AttributeError) as the_exception:
        _config_obj = config_obj.FOO
    assert the_exception.type is AttributeError


def test_bad_application_root(test_config_data, caplog) -> None:
    """
    Test a bad APPLICATION_ROOT value
    """
    orig, _expected = test_config_data

    orig["APPLICATION_ROOT"] = {"foo": "bar"}
    caplog.clear()
    with pytest.raises(ValueError) as the_exception:
        _config_obj = ResumeConfigLoader(orig)
    assert the_exception.type is ValueError
    assert "Config validation failed!" in caplog.text
    assert "Config validation error: APPLICATION_ROOT" in caplog.text
    assert (
        "Config validation error: APPLICATION_ROOT - must be of string type"
        in caplog.text
    )


def test_bad_bind_addrs(test_config_data, caplog) -> None:
    """
    Test a bad BIND_ADDRS value
    """
    orig, _expected = test_config_data

    orig["BIND_ADDRS"] = {"foo": "bar"}
    caplog.clear()
    with pytest.raises(ValueError) as the_exception:
        _config_obj = ResumeConfigLoader(orig)
    assert the_exception.type is ValueError
    assert "Config validation failed!" in caplog.text
    assert "Config validation error: BIND_ADDRS" in caplog.text
    assert "value does not match regex" in caplog.text


def test_bad_bind_port(test_config_data, caplog) -> None:
    """
    Test a bad BIND_PORT value
    """
    orig, _expected = test_config_data

    orig["BIND_PORT"] = "abc"

    caplog.clear()

    with pytest.raises(ValueError) as the_exception:
        _config_obj = ResumeConfigLoader(orig)

    assert the_exception.type is ValueError
    assert "Config validation failed!" in caplog.text
    assert "Config validation error: BIND_PORT - must be of integer type" in caplog.text


def test_bad_data_path(test_config_data, caplog) -> None:
    """
    Test a bad DATA_PATH value
    """
    orig, _expected = test_config_data

    orig["DATA_PATH"] = ["foo"]

    caplog.clear()

    with pytest.raises(ValueError) as the_exception:
        _config_obj = ResumeConfigLoader(orig)

    assert the_exception.type is ValueError
    assert "Config validation failed!" in caplog.text
    assert "Config validation error: DATA_PATH - must be of string type" in caplog.text


def test_bad_log_level(test_config_data, caplog) -> None:
    """
    Test a bad LOG_LEVEL value
    """
    orig, _expected = test_config_data

    orig["LOG_LEVEL"] = "foo"

    caplog.clear()

    with pytest.raises(ValueError) as the_exception:
        _config_obj = ResumeConfigLoader(orig)

    assert the_exception.type is ValueError
    assert "Config validation failed!" in caplog.text
    assert "Config validation error: LOG_LEVEL - unallowed value foo" in caplog.text


def test_bad_preferred_url_scheme(test_config_data, caplog) -> None:
    """
    Test a bad PREFERRED_URL_SCHEME value
    """
    orig, _expected = test_config_data

    orig["PREFERRED_URL_SCHEME"] = "foo"

    caplog.clear()

    with pytest.raises(ValueError) as the_exception:
        _config_obj = ResumeConfigLoader(orig)

    assert the_exception.type is ValueError
    assert "Config validation failed!" in caplog.text
    assert (
        "Config validation error: PREFERRED_URL_SCHEME - unallowed value foo"
        in caplog.text
    )


def test_bad_secret_key(test_config_data, caplog) -> None:
    """
    Test a bad SECRET_KEY value
    """
    orig, _expected = test_config_data

    orig["SECRET_KEY"] = 1

    caplog.clear()

    with pytest.raises(ValueError) as the_exception:
        _config_obj = ResumeConfigLoader(orig)

    assert the_exception.type is ValueError
    assert "Config validation failed!" in caplog.text
    assert "Config validation error: SECRET_KEY - must be of string type" in caplog.text


def test_bad_server_name(test_config_data, caplog) -> None:
    """
    Test a bad SERVER_NAME value
    """
    orig, _expected = test_config_data

    orig["SERVER_NAME"] = "1xa#"

    caplog.clear()

    with pytest.raises(ValueError) as the_exception:
        _config_obj = ResumeConfigLoader(orig)

    assert the_exception.type is ValueError
    assert "Config validation failed!" in caplog.text
    assert "Config validation error: SERVER_NAME" in caplog.text
    assert "value does not match regex" in caplog.text

    orig["SERVER_NAME"] = {"foo": "bar"}

    caplog.clear()

    with pytest.raises(ValueError) as the_exception:
        _config_obj = ResumeConfigLoader(orig)

    assert the_exception.type is ValueError
    assert "Config validation failed!" in caplog.text
    assert (
        "Config validation error: SERVER_NAME - must be of string type" in caplog.text
    )
