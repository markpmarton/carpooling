"""
This module builds the Flask app from other components.

The goal of this refactor was to create a more structured
and modular application.
The main application functions were separated into different
independent modules and were generalized to provide higher
level of reusability.

The implementation also utilizes best practices
(eg. independent logging and config handler module, input validation)
"""

from flask import Flask

from .controllers import bind_controllers
from .middlewares import ContentTypeMiddleware

from utils.logger import LoggerFactory

from utils.config_manager import (
    create_config,
    ConfigType,
    get_config_class_full_namespace,
)

from utils.config_manager.exceptions import InvalidConfigTypeException


def bind_logger(app):
    """
    Generates a logger based on the selected Config class.
    Then it used it as the Flask app default logger.
    """
    app.logger = LoggerFactory.get_logger(
        app.config["LOG_FILE"],
        app.config["LOG_LEVEL"],
        app.config["LOG_WORKING_DIR"],
    )

    return app


def bind_controller(app):
    """
    Forwards the controller binding to the inner method.
    """
    bind_controllers(app)
    return app


def bind_middlewares(app):
    """
    Adds the content-type checker middleware to the app.
    """
    app.wsgi_app = ContentTypeMiddleware(app)
    return app


def create_app():
    """
    Creates the base Flask app.
    """
    app = Flask(__name__, instance_relative_config=True)
    return app


def get_app():
    """
    Returns the created Flask app object.
    """
    app = create_app()
    config = None
    try:
        config = create_config(ConfigType.Development)
    except InvalidConfigTypeException as e:
        app.logger.critical(e)
        exit(1)
    app.config.from_object(get_config_class_full_namespace(config))
    app = bind_logger(app)
    app = bind_middlewares(app)
    app = bind_controller(app)

    return app
