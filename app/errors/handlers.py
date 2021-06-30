# -*- coding: utf-8 -*-
"""
    Module for setting up error handlers
"""
from flask import render_template, request, Response
from app.errors import bp
from app.api.errors import error_response as api_error_response

def wants_json_response() -> bool:
    """
    Returns whether a request wants a json response or html response
    """
    return request.accept_mimetypes['application/json'] >= \
        request.accept_mimetypes['text/html']

@bp.app_errorhandler(404)
def not_found_error(error:str) -> Response:
    """
    Error handler for 404 not found errors
    
    Args:
        error (str): The error being thrown
    """
    if wants_json_response():
        return api_error_response(404)
    return render_template('errors/404.html'), 404

@bp.app_errorhandler(500)
def internal_error(error:str) -> Response:
    """
    Error handler for 500 internal server errors
    
    Args:
        error (str): The error being thrown
    """
    if wants_json_response():
        return api_error_response(500)
    return render_template('errors/500.html'), 500