"""
    Module for configuration
"""
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

class Config(object):
    # App configuration
    VERSION = os.environ.get("VERSION") or "TEST"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "SECRET"

    # Email Configuration
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 25)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") is not None
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL") is not None
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    ADMINS = os.environ.get("MAIL_ADMINS").split(",") if os.environ.get("MAIL_ADMINS") is not None else []

    # Logging Configuration
    LOG_TO_STDOUT = os.environ.get("LOG_TO_STDOUT")