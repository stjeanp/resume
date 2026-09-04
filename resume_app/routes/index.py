"""Render the index page"""

import io

from flask import (
    Blueprint,
    current_app,
    make_response,
    render_template,
    request,
)
from werkzeug.wrappers import Response
from weasyprint import HTML  # type: ignore

index_bp = Blueprint("index_bp", __name__)


@index_bp.route("/", methods=["GET"])
def index() -> str:
    """
    Generate our index page

    :return: The rendered page
    :rtype: str
    """
    return render_template(
        "index.html",
        the_resume=current_app.extensions["resume"],
        show_menu=True,
    )


@index_bp.route("/PatStJean_Resume.pdf", methods=["GET"])
def download_pdf() -> Response:
    """
    Dynamically render the PDF version of the resume and return it to the user

    :return: The Response object containing the rendered PDF
    :rtype: Response
    """
    the_html = render_template(
        "index.html",
        the_resume=current_app.extensions["resume"],
        show_menu=False,
    )

    pdf_file = io.BytesIO()
    HTML(string=the_html).write_pdf(target=pdf_file)
    pdf_file.seek(0)

    response = make_response(pdf_file.read())
    response.headers.set("Content-Type", "Application/PDF")
    response.headers.set(
        "Content-Disposition", "attachment", filename="PatStJean_Resume.pdf"
    )
    return response
