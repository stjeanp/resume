"""
Tests for app level stuff
"""

import pytest

from flask import Flask

from resume_app import create_app


def test_app_no_configs():
    with pytest.raises(ValueError) as the_exception:
        _my_app = create_app(None)
    assert the_exception.type is ValueError


def test_app_good_configs(test_config_data):
    the_configs, _expected_configs = test_config_data
    my_app = create_app(the_configs)
    assert isinstance(my_app, Flask)
