"""
Tests for the favicon route
"""

import hashlib

import pytest


def test_favicon(client):
    """
    Make sure a get returns the right content
    """
    response = client.get("/favicon.ico")
    expected = "eb06f4b21a7ea660a933554981b02b8638e4ea2337bd87bdfca3ff963d644d27"
    actual = hashlib.sha256(response.data).hexdigest()
    assert actual == expected
