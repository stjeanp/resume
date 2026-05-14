"""
Class implementing a Resume object
"""

import json
import logging
import os
from typing import Optional

from jsonschema import validate
from jsonschema.exceptions import ValidationError, SchemaError


class Resume:
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

        if not src:
            logger.error("Invalid resume data path supplied")
            raise ValueError("Invalid value for resume path")

        if not isinstance(src, str):
            logger.error("Invalid resume data path supplied")
            raise TypeError("Invalid resume path supplied")

        if not os.path.exists(src):
            logger.error("Invalid resume data path supplied")
            raise FileNotFoundError(f"Could not find {src}")

        with open("schemas/resume.schema.json", "r") as resume_schema:
            resume_schema = json.load(resume_schema)

        with open(src, "r") as resume_src:
            resume_data = json.load(resume_src)

        try:
            validate(instance=resume_data, schema=resume_schema)
        except SchemaError:
            logger.error("There is something wrong in the schema")
            raise
        except ValidationError:
            logger.error("The resume data failed schema validation")
            raise

        self.__data = resume_data

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
