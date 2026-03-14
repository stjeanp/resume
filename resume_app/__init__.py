"""App startup"""
import os

from dotenv import load_dotenv
from flask import Flask

from .helpers.resume import Resume
from .routes.favicon import favicon_bp
from .routes.index import index_bp


def create_app() -> Flask:
    """
    Create our application and do all initialization and setup

    :return: The initialized app
    :rtype: Flask
    """
    load_dotenv()

    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.extensions["resume"] = Resume(os.getenv("RESUME_PATH", ""))

    app.register_blueprint(favicon_bp)
    app.register_blueprint(index_bp)

    return app
