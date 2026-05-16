"""
Tests of the Flask error handlers
"""

import pytest


def test_index_get(client):
    response = client.get("/")
    assert response.status_code == 200

def test_index_get_pdf(client):
    response = client.get("/PatStJean_Resume.pdf")
    assert response.status_code == 200
