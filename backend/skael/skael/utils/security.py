from datetime import datetime, timedelta

import jwt
import requests
import uuid

from flask import current_app
from skael.DAOs.user_dao import UserDAO
from skael.models import db
from skael.models.user_table import UserTable as User


class FlaskJWTWrapper(object):
    """
    Acts as a wrapper for flask jwt methods.
    """
    @staticmethod
    def authenticate(username, password):
        user = UserDAO().get_by_username(username)
        if User.bcrypt_compare(password, user.password):
            jwt_claim = uuid.uuid4()
            db.session.query(
                User
            ).filter_by(
                public_id=user.public_id
            ).update({
                'jwt_claim': jwt_claim
            })
            db.session.commit()

            user.jwt_claim = jwt_claim
            return user

    @staticmethod
    def identify(payload):
        return db.session.query(
            User
        ).filter_by(
            public_id=payload['identity'],
            jwt_claim=payload['jwt_claim']
        ).first()

    @staticmethod
    def create_jwt(app, identity, *, keep_logged_in=False):
        iat = datetime.utcnow()
        nbf = iat + app.config.get('JWT_NOT_BEFORE_DELTA')

        if keep_logged_in:
            exp = iat + timedelta(seconds=2592000)
        else:
            exp = iat + app.config.get('JWT_EXPIRATION_DELTA')

        return {
            'exp': exp,
            'iat': iat,
            'nbf': nbf,
            'identity': identity.public_id,
            'jwt_claim': str(identity.jwt_claim)
        }

    @staticmethod
    def sign_jwt(_jwt):
        return jwt.encode(_jwt, current_app.config['SECRET_KEY'])
