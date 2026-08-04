"""Configs for gunicorn"""

import os

from dotenv import dotenv_values

from resume_app.helpers.config import ResumeConfigLoader

config_file = os.getenv("CONFIG_FILE", ".env")
app_configs = ResumeConfigLoader(dotenv_values(config_file)).configs

if app_configs is None:
    raise ValueError("Failed to load configs!")

pidfile = "./gunicorn.pid"  # pylint: disable=invalid-name
accesslog = "-"  # pylint: disable=invalid-name
errorlog = "-"  # pylint: disable=invalid-name
loglevel = app_configs["LOG_LEVEL"]
capture_output = False  # pylint: disable=invalid-name

bind = []
for the_addr in app_configs["BIND_ADDRS"]:
    bind.append(f"{the_addr}:{app_configs['BIND_PORT']}")
