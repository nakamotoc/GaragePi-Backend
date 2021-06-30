# -*- coding: utf-8 -*-
"""
    Module Web API
"""
from functools import wraps
from datetime import datetime
from flask import (
    request,
)

from app.api import bp

from flask_restx import Resource
import flask_restx.fields as fields
from app import rest_api
from app.gpio import press_opener_button


def token_required(f):
    """
    Wrapper function for validating jwt for API requests
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        # Check for token
        token = None
        if "X-API-KEY" in request.headers:
            token = request.headers["X-API-KEY"]
        if not token:
            return {"message": "Token is missing"}, 401

        # Check whether token is valid
        if not is_valid_auth_token(token):
            return {"message": "Invalid auth token"}, 401

        # Decode token and abort if None (indicating the token is invalid)
        token_data = decode_auth_token(token)
        if token_data is None:
            return {"message": "Malformed auth token"}, 401

        # Check authorization in payload
        is_authorized = token_data.get("authorized", False)

        if not is_authorized:
            return {"message": "Invalid credentials"}, 401

        return f(*args, **kwargs)

    return decorated


garage_door_opener_button_press_event_parser = rest_api.parser()
garage_door_opener_button_press_event_parser.add_argument(
    "press_duration",
    type=float,
    help="The duration of time to press the garage door opener button",
    location="json",
)

garage_door_opener_button_post_response = rest_api.model(
    "GarageDoorOpenerButton",
    {
        "status": fields.String(),
        "event_time": fields.DateTime(),
        "press_duration": fields.Float(min=0, exclusiveMin=True),
    },
)


@rest_api.route("/garage-door-opener-button")
@rest_api.doc()
class GarageDoorOpenerButton(Resource):
    """
    Flask RestX resource modeling a garage door opener
    """

    @rest_api.doc(
        security="apikey",
    )
    @rest_api.expect(garage_door_opener_button_press_event_parser)
    @rest_api.response(400, "Validation error")
    @rest_api.marshal_with(
        garage_door_opener_button_post_response,
        code=200,
        description="Button 'pressed'",
    )
    def post(self):
        """
        Post a garage door opener button interaction. The garage door opener model
        takes a press duration indicating how long to 'press' the garage door opener
        button.
        """
        data = request.get_json() or {}
        press_duration = data.get("press_duration", None)

        if press_duration is None:
            return {"message", "Press duration (press_duration) not specified"}, 400

        if press_duration <= 0:
            return {
                "message",
                "Press duration (press_duration) must be greater than zero seconds",
            }, 400

        press_opener_button(press_duration)

        return {
            "status": "Success",
            "event_time": datetime.now().isoformat(),
            "press_duration": press_duration,
        }, 200
