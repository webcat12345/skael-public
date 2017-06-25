import logging
from http import HTTPStatus

from flask.ext.jwt import jwt_required
from flask.views import MethodView
from flask import jsonify

from marshmallow.fields import String
from webargs.flaskparser import parser

from skael.DAOs.user_dao import UserDAO
from skael.facades.user_facade import UserFacade
from skael.utils.marshalizers import UserMarshal
from skael.utils.exceptions import EndpointException


class Users(MethodView):
    """Houses CRUD operations for user management."""

    @jwt_required()
    def get(self, user_id):
        user_info = UserDAO().get(user_id)

        if user_info is None:
            logging.error('Requested user ({0} does not exist.'.format(
                user_id
            ))

            raise EndpointException(
                'Requested user does not exist.',
                HTTPStatus.NOT_FOUND
            )

        if not user_info.is_validated:
            logging.error(
                'Requested unvalidated account: {0}'.format(user_id)
            )

            raise EndpointException(
                'Account is not validated.',
                HTTPStatus.FORBIDDEN
            )

        logging.info('Retrieved user info for {0}'.format(user_id))

        return jsonify(UserMarshal().dump(user_info).data)

    def post(self):
        arg_fields = {
            'email': String(required=True),
            'plaintext_password': String(required=True),
            'username': String(required=True)
        }
        args = parser.parse(arg_fields)

        user_info = UserFacade().create_new_user(**args)

        logging.info('Successfully created new user at {0}'.format(
            args['email']
        ))

        return jsonify(UserMarshal().dump(user_info).data)

    @jwt_required()
    def delete(self, user_id):
        user_info = UserDAO().soft_delete(
            user_id
        )

        logging.info(
            'Successfully soft deleted user {0} for requesting user.'.format(
                user_id
            )
        )

        return jsonify(UserMarshal().dump(user_info).data)

    @jwt_required()
    def put(self, user_id):
        arg_fields = {
            'email': String(),
            'current_password': String(),
            'plaintext_password': String()
        }
        args = parser.parse(arg_fields)

        user_info = UserDAO().update_user_data(user_id, **args)

        logging.info(
            'Successfully updated information for user {0}'.format(
                user_info
            )
        )

        return jsonify(UserMarshal().dump(user_info).data)


def export_routes(_app):
    _app.add_url_rule(
        '/users/<string:user_id>',
        view_func=Users.as_view('api_v1_users_update_user'),
        methods=['GET', 'DELETE', 'PUT']
    )

    _app.add_url_rule(
        '/users/',
        view_func=Users.as_view('api_v1_users_new_user'),
        methods=['POST']
    )
