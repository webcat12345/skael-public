import logging
from flask.views import MethodView
from flask import jsonify

from marshmallow.fields import String
from webargs.flaskparser import parser

from skael.DAOs.user_dao import UserDAO
from skael.facades.user_facade import UserFacade
from skael.utils.marshalizers import UserMarshal


class ResetPassword(MethodView):
    """
    Handles anything related to resetting a password
    """

    def post(self):
        """
        Reset a users password.
        """
        arg_fields = {
            'token': String(required=True),
            'plaintext_password': String(required=True)
        }
        args = parser.parse(arg_fields)

        validated_user = UserDAO().reset_user_password(**args)

        logging.info(
            'Successfully validated token {0} for user {1}.'.format(
                args['token'],
                validated_user,
            )
        )

        return jsonify(UserMarshal().dump(validated_user).data)

    def put(self):
        """
        Regenerate the reset password
        """
        arg_fields = {
            'email': String(required=True),
        }
        args = parser.parse(arg_fields)

        UserFacade().regenerate_reset_password_token(args['email'])

        logging.info('Successfully regenerated token')

        return jsonify({'success': True})


def export_routes(_app):
    _app.add_url_rule(
        '/users/reset_password',
        view_func=ResetPassword.as_view('api_v1_users_reset'),
        methods=['POST', 'PUT']
    )
