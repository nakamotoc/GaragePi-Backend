#-*- coding: utf-8 -*-
"""
Module for handling api errors as json responses
"""
from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

def error_response(status_code:int, message:str=None):
    """
    Provides a JSON error response when provided with a status code and message.
    Args:
        status_code (int): The status code to return in the json object
        message (str): The message to return in the json object
    
    Returns:
        A json object with the containing the error message and the response status code
    
    """
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response

def bad_request(message:str):
    """
    Provides a bad request 400 response with a provided message.
    Args:
        message (str): The message to return in the json error response
    
    Returns:
        A bad request 400 json object response with a provided message
    
    """
    return error_response(400, message)