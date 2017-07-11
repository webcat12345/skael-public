from http import HTTPStatus

from flask import current_app
from flask_jwt import current_identity

from skael.utils.security import FlaskJWTWrapper


def start_lifecycle_hooks(_app):
    @_app.after_request
    def process_jwt_token(response):
        """
        Handles refreshing and creating a new JWT.

        :param flask.Response response:
        :rtype: str
        :return: The response.
        """
        if response.status_code == HTTPStatus.OK and current_identity:
            response.headers['new_jwt'] = '{0}'.format(
                str(__encode_token().decode('utf-8'))
            )

        return response


def __encode_token():
    jwt = FlaskJWTWrapper.create_jwt(current_app, current_identity)
    return FlaskJWTWrapper.sign_jwt(jwt)
