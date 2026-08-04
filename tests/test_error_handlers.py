"""
Tests of the Flask error handlers
"""

import logging
from flask import url_for


def test_not_found_exception(client, caplog):
    """
    Test handling a NotFound exception
    """
    caplog.clear()
    caplog.set_level(logging.DEBUG)
    response = client.get("/not_a_page.html")
    assert response.status_code == 302
    assert response.location == url_for("index_bp.index", _external=False)
    assert "Not Found" in caplog.text
    assert "/not_a_page.html" in caplog.text


def test_method_not_allowed_exception(client, caplog):
    """
    Test handling a MethodNotAllowed exception
    """
    caplog.clear()
    caplog.set_level(logging.DEBUG)
    response = client.post("/")
    assert response.status_code == 302
    assert response.location == url_for("index_bp.index", _external=False)
    assert "Method Not Allowed" in caplog.text


def test_direct_error_page(client, caplog):
    """
    Test trying to access the error page directly
    """
    caplog.clear()
    caplog.set_level(logging.DEBUG)
    response = client.get("/error.html")
    assert response.status_code == 302
    assert response.location == url_for("index_bp.index", _external=False)


def mock_a_fatal_exception():
    """
    Used to raise a fatal exception for testing
    """
    raise RuntimeError("Testing")


def test_fatal_exception(app, caplog):
    """
    Test handling a fatal application exception
    """
    app.config.update({"PROPAGATE_EXCEPTIONS": False})
    app.view_functions["index_bp.index"] = mock_a_fatal_exception
    caplog.clear()
    caplog.set_level(logging.DEBUG)
    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 500
        assert b"Oh no!" in response.data
        assert url_for("index_bp.index", _external=False).encode() in response.data
        assert "Fatal Error" in caplog.text
