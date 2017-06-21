import logging
from flask.views import MethodView
from flask import jsonify

from marshmallow.fields import String
from webargs.flaskparser import parser

from skael.DAOs.user_dao import UserDAO
from skael.facades.user_facade import UserFacade
from skael.utils.marshalizers import UserMarshal


class VerificationToken(MethodView):
    """
    Handles anything related to the verification token.
    """

    def post(self):
        """
        Validate a user by providing the correct token.
        """
        arg_fields = {
            'token': String(required=True),
        }
        args = parser.parse(arg_fields)

        validated_user = UserDAO().verify_token(args['token'])

        logging.info(
            'Successfully validated token {0} for user {1}.'.format(
                args['token'],
                validated_user,
            )
        )

        return jsonify(UserMarshal().dump(validated_user).data)

    def put(self):
        """
        Regenerate the verification token.
        """
        arg_fields = {
            'email': String(required=True),
        }
        args = parser.parse(arg_fields)

        UserFacade().regenerate_verification_token(args['email'])

        logging.info('Successfully regenerated token')

        return jsonify({'success': True})


def export_routes(_app):
    _app.add_url_rule(
        '/users/verify',
        view_func=VerificationToken.as_view('api_v1_users_verification'),
        methods=['POST', 'PUT']
    )
