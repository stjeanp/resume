"""
Tests of the resume helper class
"""

import logging

from json.decoder import JSONDecodeError
from jsonschema.exceptions import SchemaError, ValidationError
import pytest

from resume_app.helpers.resume import Resume


def test_resume_init(test_config_data, caplog):
    my_configs, _expected = test_config_data

    the_resume = Resume()
    assert isinstance(the_resume, Resume)
    assert the_resume.is_initialized is False

    with pytest.raises(
        ValueError,
        match="Invalid resume data path supplied",
    ) as the_exception:
        the_resume.initialize("")
    assert the_exception.type is ValueError

    with pytest.raises(
        TypeError,
        match="Invalid resume data path supplied",
    ) as the_exception:
        the_resume.initialize(1)
    assert the_exception.type is TypeError

    with pytest.raises(
        FileNotFoundError,
        match="Invalid resume data path supplied",
    ) as the_exception:
        the_resume.initialize("./file_not_found")
    assert the_exception.type is FileNotFoundError

    with pytest.raises(SchemaError) as the_exception:
        bad_schema = Resume()
        bad_schema.SCHEMA_PATH = "tests/test_data/bad.resume.schema.json"
        bad_schema.initialize(my_configs["DATA_PATH"])
    assert the_exception.type is SchemaError

    with pytest.raises(JSONDecodeError) as the_exception:
        _bad_json_decode = Resume("tests/test_data/bad.decode.resume.json")
    assert the_exception.type is JSONDecodeError

    with pytest.raises(ValidationError) as the_exception:
        _bad_json_decode = Resume("tests/test_data/bad.resume.json")
    assert the_exception.type is ValidationError

    the_resume = Resume(my_configs["DATA_PATH"])
    assert isinstance(the_resume, Resume)
    assert the_resume.is_initialized is True

    caplog.clear()
    the_resume.initialize(my_configs["DATA_PATH"])
    assert "initialize called on an already initialized instance" in caplog.text
