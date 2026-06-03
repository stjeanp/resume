"""Our app startup"""

import logging
import os

from dotenv import dotenv_values

from resume_app import create_app
from resume_app.helpers.config import ResumeConfigLoader

config_file = os.getenv("CONFIG_FILE", ".env")
app_configs = ResumeConfigLoader(dotenv_values(config_file)).configs

if app_configs is None:
    raise ValueError("Failed to load configs!")

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] [%(name)s.%(funcName)s] %(message)s",
    level=app_configs["LOG_LEVEL"],
)

app = create_app(app_configs)
