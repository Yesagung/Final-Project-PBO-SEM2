from logging.config import dictConfig

import config
from flask import Flask, abort, current_app
from flask_cors import CORS
from utils import db, ma, bcrypt, jwt
from route.user import authz_blueprint
from route.course import course_blueprint
# TODO: add any route here
# from route.anything import anything_blueprint ##here

from mongoengine.errors import DoesNotExist, ValidationError, NotUniqueError
from requests.exceptions import ConnectionError

def create_app():
    dictConfig(config.LOG_CONFIG)
    app = Flask(__name__)
    CORS(app)
    app.debug = config.DEBUG
    app.config["MONGODB_SETTINGS"] = {
        'host': config.DB_URI
    }
    app.config['JWT_SECRET_KEY'] = config.SECRET_KEY
    
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)


    app.register_blueprint(
        authz_blueprint,
        url_prefix=f"/api/{config.CURRENT_VERSION_API}/",
    )
    app.register_blueprint(
        course_blueprint,
        url_prefix=f"/api/{config.CURRENT_VERSION_API}/"
    )

    @app.errorhandler(DoesNotExist)
    def handle_not_exist_record(e):
        current_app.logger.error(str(e))
        abort(404, "Resource not exist")
    
    @app.errorhandler(ValidationError)
    def handle_mongo_validation_error(e):
        current_app.logger.error(str(e))
        abort(403, "Invalid format")
    
    @app.errorhandler(NotUniqueError)
    def handle_not_unique(e):
        # TODO: Please make it more general
        abort(400, str(e))

    @app.errorhandler(ConnectionError)
    def handle_request_connection_error(e):
        current_app.logger.error(str(e))
        abort(422, "Connection error: Possible cause by server dead or wrong third party IP/Port")
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host=config.HOST, port=config.PORT)



