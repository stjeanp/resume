"""
Tests of the Flask error handlers
"""


def test_index_get(client):
    """
    Test a friendle neighbourhood GET of the index page
    """
    response = client.get("/")
    assert response.status_code == 200


def test_index_get_pdf(client):
    """
    Test the render+download link for the PDF version. This is here because
    it also uses the index.html template and lives in the index_bp blueprint
    """
    response = client.get("/PatStJean_Resume.pdf")
    assert response.status_code == 200
