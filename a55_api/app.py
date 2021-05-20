from flask import Flask
from flask.helpers import get_debug_flag

from a55_api.extensions import db, migrate
from a55_api.utils import log

from a55_api.credit_request.routes import creditRequestBlueprint
from a55_api.user.routes import userBlueprint
from a55_api.settings import DevConfig, ProdConfig

from a55_api.exceptions import A55ApiError, generic_bad_request, generic_system_error


def create_app(config_object=None):
    if not config_object:
        config_object = DevConfig if get_debug_flag() else ProdConfig

    log.info(f"Creating Flask app on {config_object.ENV}")
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Initializing database
    log.info("Initializing database")
    db.init_app(app)
    migrate.init_app(app, db)

    # Registering error handlers
    log.info("Registering error handlers")
    register_custom_errorhandler(app)
    app.register_error_handler(400, generic_bad_request)
    app.register_error_handler(500, generic_system_error)

    # Registering blueprints
    log.info("Registering blueprints")
    app.register_blueprint(creditRequestBlueprint)
    app.register_blueprint(userBlueprint)

    return app


def register_custom_errorhandler(app):

    def errorhandler(error):
        response = error.to_json()
        response.status_code = error.status_code
        return response

    app.errorhandler(A55ApiError)(errorhandler)
