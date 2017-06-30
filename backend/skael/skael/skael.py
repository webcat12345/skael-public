import codecs
import logging
import sys

from flask import Flask, jsonify
from flask_jwt import JWT
from datetime import datetime

from skael.utils.security import FlaskJWTWrapper
from skael.models import db

from skael.api import user_export_routes
from skael.api import reset_export_routes
from skael.api import verify_export_routes
from skael.utils.error_handler import register_error_handlers


# TODO(ian): Finish the `config_file` nonsense
def create_app(config_file=None):
    """
    An application factory used to generate application contexts.

    :param config_file:
    :rtype: Flask
    :return: An application context which can be used for uwsgi runtimes or
    unit tests.
    """
    app = Flask(__name__)
    app.config.from_object('skael.config.Config')

    jwt = JWT(app, FlaskJWTWrapper.authenticate, FlaskJWTWrapper.identify)

    @jwt.jwt_payload_handler
    def jwt_handler(identity):
        iat = datetime.utcnow()
        exp = iat + app.config.get('JWT_EXPIRATION_DELTA')
        nbf = iat + app.config.get('JWT_NOT_BEFORE_DELTA')
        return {
            'exp': exp,
            'iat': iat,
            'nbf': nbf,
            'identity': identity.public_id,
            'jwt_claim': str(identity.jwt_claim)
        }

    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s] %(levelname)-8s [%(name)s] %(message)s",
        stream=(codecs.getwriter("utf-8")(sys.stdout.buffer, "replace")
                                if hasattr(sys.stdout, "buffer")
                                else None))

    with app.app_context():

        user_export_routes(app)
        verify_export_routes(app)
        reset_export_routes(app)

        # This is just a test will be removed in production
        # to follow best practises
        @app.route("/api/hello")
        def hello():
            print(list(app.url_map.iter_rules()))
            res = db.session.execute("select version()")
            postgres_version = list(res)[0][0]
            return jsonify(response="Hello, World!", postgres_version=postgres_version)
            

        register_error_handlers(app)

        db.init_app(app)
        app.db = db

    return app
