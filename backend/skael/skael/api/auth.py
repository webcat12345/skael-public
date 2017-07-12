import logging

from flask.ext.jwt import jwt_required
from flask.views import MethodView
from flask import jsonify

from skael.DAOs.user_dao import UserDAO


class Authentication(MethodView):
    """
    Handles logging a user out. Logging in is enforced by the Flask-JWT
    package.
    """

    @jwt_required()
    def delete(self):
        """
        Logs a user out and invalidates their JWT.
        """
        UserDAO().logout_current_user()

        logging.info('Successfully logged out user')

        return jsonify({'success': True})

    @jwt_required()
    def get(self):
        """
        Verifies a JWT is still valid.
        """
        return jsonify({'success': True})


def export_routes(_app):
    _app.add_url_rule(
        '/users/auth',
        view_func=Authentication.as_view('api_v1_auth'),
        methods=['DELETE', 'GET']
    )
