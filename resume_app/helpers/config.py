"""
Config helper class for validation
"""

import logging
from typing import Any, Final, Optional

from cerberus import Validator  # type: ignore


def make_list(the_val: str) -> list:
    """
    Used to coerce comma separated .env values to a list

    :param: the_val
    :type the_val: str
    :return: The split up list
    :rtype: list
    """
    the_list = [v.strip() for v in the_val.split(",") if v]
    return the_list


class ResumeConfigLoader:
    """
    Class to load and validate the resume app's configs
    """

    THE_SCHEMA: Final[dict] = {
        "APPLICATION_ROOT": {
            "type": "string",
            "default": "/",
            "required": True,
            "nullable": False,
            "empty": False,
        },
        "BIND_ADDRS": {
            "type": "list",
            "default": "[::]",
            "required": True,
            "schema": {
                "type": "string",
                "empty": False,
                "regex": r"^[a-zA-Z0-9:\.\[\]\-]+$",
                "nullable": False,
            },
            "minlength": 1,
            "nullable": False,
            "empty": False,
            "coerce": (str, make_list),
        },
        "BIND_PORT": {
            "type": "integer",
            "default": 2112,
            "required": True,
            "nullable": False,
            "min": 1025,
            "max": 65535,
            "coerce": int,
        },
        "DATA_PATH": {
            "type": "string",
            "default": "data/resume.json",
            "required": True,
            "nullable": False,
            "empty": False,
        },
        "LOG_LEVEL": {
            "type": "string",
            "default": "INFO",
            "allowed": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            "required": True,
            "nullable": False,
            "empty": False,
        },
        "PREFERRED_URL_SCHEME": {
            "type": "string",
            "default": "http",
            "allowed": ["http", "https"],
            "required": True,
            "nullable": False,
            "empty": False,
        },
        "SECRET_KEY": {
            "type": "string",
            "default": "InsecurePleaseChange",
            "required": True,
            "nullable": False,
            "empty": False,
        },
        "SERVER_NAME": {
            "type": "string",
            "default": "localhost",
            "regex": r"^[a-zA-Z0-9\.\-]+$",
            "required": True,
            "nullable": False,
            "empty": False,
        },
    }

    def __init__(self, raw_configs: dict) -> None:
        """
        Class initializer for ResumeConfigLoader class

        :param raw_configs: Raw config data dictionary
        :type raw_configs: dict

        :raises: ValueError when the raw config data has errors

        :return: Nothing
        :rtype: None
        """
        self.__configs = None

        logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

        v = Validator()
        v.allow_unknown = False
        if not v.validate(raw_configs, self.THE_SCHEMA):
            logger.critical("Config validation failed!")
            for the_error in v.errors:
                for error_message in v.errors[the_error]:
                    logger.critical(
                        "Config validation error: %s - %s", the_error, error_message
                    )
            raise ValueError("Config validation failed!")
        self.__configs = v.document

    def __getattr__(self, attr: str) -> Any:
        """
        Override default __getattr__ so that we don't have to define a
        ton of properties

        :param attr: The attribute name
        :type attr: str

        :raises AttributeError: The attribute was not found

        :return: The attribute's value, if found
        :rtype: Any
        """
        if self.configs and attr in self.configs.keys():
            return self.configs[attr]
        raise AttributeError(f"No attribute named {attr} found")

    @property
    def configs(self) -> Optional[dict[str, Any]]:
        """
        Return the dict of parsed and validated configs

        :return: The dict of parsed and validated configs
        :rtype: Optional[dict[str, Any]]
        """
        return self.__configs
