from datetime import datetime
import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask
from flask.json import JSONEncoder
from config import Config
from flask_restx import Api
from flask_cors import CORS

api_authorizations = {"apikey": {"type": "apiKey", "in": "header", "name": "X-API-KEY"}}
rest_api = Api(
    version="1.0",
    title="GaragePI API",
    description="An API for interacting with the GaragePI hardware",
    authorizations=api_authorizations,
    default="GaragePi",
    default_label="GaragePi-API",
)
cors = CORS()


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


def create_app(config_class=Config):
    """
    Factory function to create app contexts
    """
    app = Flask(__name__)

    app.json_encoder = CustomJSONEncoder

    app.config.from_object(config_class)
    app.config.VERSION = config_class.VERSION

    cors.init_app(app, resources={r"/api/*": {"origins": ["http://localhost","http://mimeticmaker.com"]}})

    # Blueprints
    from app.errors import bp as errors_bp

    app.register_blueprint(errors_bp)

    from app.api import bp as api_bp

    rest_api.init_app(api_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    # Configure logging and e-mail if not debugging
    if False:
        if app.config["MAIL_SERVER"]:
            auth = None
            if app.config["MAIL_USERNAME"] or app.config["MAIL_PASSWORD"]:
                auth = (app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"])
            secure = None
            if app.config["MAIL_USE_TLS"]:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config["MAIL_SERVER"], app.config["MAIL_PORT"]),
                fromaddr="no-reply@" + app.config["MAIL_SERVER"],
                toaddrs=app.config["ADMINS"],
                subject="GaragePi API Failure",
                credentials=auth,
                secure=secure,
            )
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if app.config["LOG_TO_STDOUT"]:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists("logs"):
                os.mkdir("logs")
            file_handler = RotatingFileHandler(
                "logs/garagepi_api.log", maxBytes=10240, backupCount=10
            )
            file_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s %(levelname)s: %(message)s "
                    "[in %(pathname)s:%(lineno)d]"
                )
            )
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info("GaragePi API startup")

    return app