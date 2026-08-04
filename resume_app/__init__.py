"""App startup"""

import logging
import os
import random
import time
from typing import Any, Optional, Tuple

from flask import Flask, redirect, render_template, request, url_for
import werkzeug.exceptions
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.wrappers import Response

from .helpers.resume import Resume
from .routes.error import error_bp
from .routes.favicon import favicon_bp
from .routes.index import index_bp


def register_error_handlers(app: Flask) -> None:
    """
    Register error handlers here due to app factory pattern

    :param app: The Flask app
    :type app: Flask
    :return: Nothing
    :rtype: None
    """

    @app.errorhandler(werkzeug.exceptions.NotFound)
    @app.errorhandler(werkzeug.exceptions.MethodNotAllowed)
    def non_fatal_error_handler(e: Exception) -> Response:
        """
        Handles all non-fatal errors by redirecting the visitor back
        to the index page.

        :param e: The exception
        :type e: Exception
        :return: The redirect response
        :rtype: Response
        """
        msg_txt = "Unknown error"
        log_level = logging.ERROR
        match e:
            case werkzeug.exceptions.NotFound():
                msg_txt = "Not Found"
                log_level = logging.INFO
            case werkzeug.exceptions.MethodNotAllowed():
                msg_txt = "Method Not Allowed"
        app.logger.log(
            log_level,
            "%s: URL: %s, Method: %s, Remote Addr: %s, Referrer: %s",
            msg_txt,
            request.url,
            request.method,
            request.remote_addr,
            request.referrer,
        )
        return redirect(url_for("index_bp.index"), 302)

    @app.errorhandler(werkzeug.exceptions.InternalServerError)
    def fatal_error_handler(e: Exception) -> tuple[str, int]:
        """
        Handles all fatal errors by displaying an error page

        :param e: The exception
        :type e: Exception
        :return: The rendered error page
        :rtype: tuple[str, int]
        """
        app.logger.error(
            "Fatal Error: URL: %s, Method: %s, Remote Addr: %s, Referrer: %s, Exception: %s",
            request.url,
            request.method,
            request.remote_addr,
            request.referrer,
            e,
        )
        return (render_template("error.html"), 500)


def create_app(configs: Optional[dict[str, Any]] = None) -> Flask:
    """
    Create our application and do all initialization and setup

    :param configs: The app configs dict
    :type configs: Optional[dict[str, Any]]

    :raises ValueError: Invalid configs dict passed in

    :return: The initialized app
    :rtype: Flask
    """
    if not configs or not isinstance(configs, dict):
        raise ValueError("Invalid configs passed in")

    # Random pause to let gunicorn workers complete startup
    short_pause = random.randint(100, 500) / 1000
    time.sleep(short_pause)

    logger = logging.getLogger(name=__name__)
    logger.info("Starting resume app...")

    app = Flask(__name__.split(",", maxsplit=1)[0])
    app.config.from_mapping(configs)

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)  # type: ignore[method-assign]

    app.extensions["resume"] = Resume(configs["DATA_PATH"])

    register_error_handlers(app)

    app.register_blueprint(error_bp)
    app.register_blueprint(favicon_bp)
    app.register_blueprint(index_bp)

    return app
