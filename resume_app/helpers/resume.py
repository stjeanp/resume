"""
Class implementing a Resume object
"""

import json
import logging
import os
from typing import Optional

from json.decoder import JSONDecodeError
from jsonschema import validate
from jsonschema.exceptions import ValidationError, SchemaError
from referencing.exceptions import Unresolvable


class Resume:
    SCHEMA_PATH = "schemas/resume.schema.json"

    def __init__(self, src: Optional[str] = None) -> None:
        """
        Initialize a resume class from the JSON data in the file passed to us

        :param src: The path to the resume data
        :type src: Optional[str]

        :return: Nothing
        :rtype: None

        :raises FileNotFoundError: If the file doesn't exist
        :raises ValueError: If src is invalid
        """
        self.__initialized = False
        self.__data: dict = {}

        if src is None:
            return

        self.initialize(src)

    @property
    def is_initialized(self) -> bool:
        """
        Returns the instance's initialized state

        :return: Whether this instance has been initialized yet
        :rtype: bool
        """
        return self.__initialized

    def initialize(self, src: str) -> None:
        """
        Initialize the Resume object

        :param src: The path to the resume data
        :type src: str

        :raises ValueError: The src param is invalid
        :raises TypeError: The src param is invalid
        :raises FileNotFoundError: The file doesn't exist
        :raises ValidationError: The file did not pass schema validation

        :return: Nothing
        :rtype: None
        """
        logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

        if self.is_initialized:
            logger.warning("initialize called on an already initialized instance")
            return

        msg = "Invalid resume data path supplied"
        if not src:
            logger.error(msg)
            raise ValueError(msg)

        if not isinstance(src, str):
            logger.error(msg)
            raise TypeError(msg)

        if not os.path.exists(src):
            logger.error(msg)
            raise FileNotFoundError(msg)

        with open(self.SCHEMA_PATH, "r") as resume_schema:
            resume_schema = json.load(resume_schema)

        try:
            with open(src, "r") as resume_src:
                resume_data = json.load(resume_src)
            validate(instance=resume_data, schema=resume_schema)
        except JSONDecodeError:
            logger.error("The resume data failed JSON decode")
            raise
        except (SchemaError, Unresolvable) as the_exception:
            logger.error("There is something wrong in the schema")
            raise SchemaError(str(the_exception))
        except ValidationError:
            logger.error("The resume data failed schema validation")
            raise

        self.__data = resume_data
        self.__initialized = True

    @property
    def name(self) -> str:
        """
        Return the name from the resume data

        :return: The name from the resume data
        :rtype: str
        """
        return self.__data["contact-info"]["name"]

    @property
    def address(self) -> dict:
        """
        Return the address data from the resume data

        :return: The address data from the resume data
        :rtype: dict
        """
        return self.__data["contact-info"]["address"]

    @property
    def email(self) -> str:
        """
        Return the email address from the resume data

        :return: The email address from the resume data
        :rtype: str
        """
        return self.__data["contact-info"]["email-address"]

    @property
    def phone(self) -> dict:
        """
        Return the phone number data from the resume data

        :return: The phone number data from the resume data
        :rtype: dict
        """
        return self.__data["contact-info"]["phone-number"]

    @property
    def about_me(self) -> dict:
        """
        Return the about-me data from the resume data

        :return: The about-me data from the resume data
        :rtype: dict
        """
        return self.__data["about-me"]

    @property
    def skills(self) -> list:
        """
        Return the skills data from the resume data

        :return: The skills data from the resume data
        :rtype: list
        """
        return self.__data["skills"]

    @property
    def education(self) -> list:
        """
        Return the education data from the resume data

        :return: The education data from the resume data
        :rtype: list
        """
        return self.__data["education"]

    @property
    def experience(self) -> list:
        """
        Return the experience data from the resume data

        :return: The experience data from the resume data
        :rtype: list
        """
        return self.__data["experience"]
