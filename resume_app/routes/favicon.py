import os
from flask import Blueprint, current_app, send_from_directory
from werkzeug.wrappers import Response

favicon_bp = Blueprint("favicon", __name__)


@favicon_bp.route("/favicon.ico", methods=["GET"])
def favicon() -> Response:
    """
    Return our favico

    :return: The favicon data
    :rtype: Response
    """
    return send_from_directory(
        os.path.join(current_app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )
