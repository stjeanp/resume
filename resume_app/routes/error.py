"""
Blueprint for the error page
"""

from flask import Blueprint, redirect, url_for
from werkzeug.wrappers import Response

error_bp = Blueprint("error_bp", __name__)


@error_bp.route("/error.html", methods=["GET"])
def error_page() -> Response:
    """
    Send anyone coming here directly right back to the index page

    :return: The redirect
    :rtype: Response
    """
    return redirect(url_for("index_bp.index"), 302)
