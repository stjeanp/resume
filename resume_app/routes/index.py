"""Render the index page"""

from flask import Blueprint, current_app, render_template

index_bp = Blueprint("index", __name__)
@index_bp.route("/")
def index():
    return render_template("index.html", the_resume=current_app.extensions["resume"])