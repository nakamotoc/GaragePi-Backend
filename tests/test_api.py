"""
Tests for API
"""
from app import rest_api
from app.api.resources import GarageDoorOpenerButton


def test_garage_opener_button_post_valid(client):
    """
    GIVEN an instance of the GaragePi API

    WHEN a POST request is made to the garage_opener_button resource with a timing specified

    THEN a success message is returned indicate the datetime the button press was completed 
    """
    response = client.post(
        rest_api.url_for(GarageDoorOpenerButton),
        json={
            "press_duration":1
        }
    )
    assert response.status_code == 200

def test_garage_opener_button_post_invalid_duration(client):
    """
    GIVEN an instance of the GaragePi API

    WHEN a POST request is made to the garage_opener_button resource with a timing specified incorrectly

    THEN a 400 response is returned
    """
    response = client.post(
        rest_api.url_for(GarageDoorOpenerButton),
        json={
            "press_duration":-1
        }
    )
    assert response.status_code == 400

def test_garage_opener_button_post_invalid_missing_parameter(client):
    """
    GIVEN an instance of the GaragePi API

    WHEN a POST request is made to the garage_opener_button resource without a timing duration specified

    THEN a 400 response is returned
    """
    response = client.post(
        rest_api.url_for(GarageDoorOpenerButton),
        json={
        }
    )
    assert response.status_code == 400

