import json
from datetime import datetime, timedelta

import jwt
import uuid

from flask import current_app, request
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
                'jwt_claim': jwt_claim,
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
    def create_jwt(app, identity):
        iat = datetime.utcnow()
        nbf = iat + app.config.get('JWT_NOT_BEFORE_DELTA')

        keep_logged_in = request.headers.get('KeepLoggedIn')
        jwt_expiration_delta = app.config.get('JWT_EXPIRATION_DELTA')

        current_jwt = request.headers.get('Authorization')
        if current_jwt:
            current_jwt = current_jwt.split(' ')[1]
            current_jwt = jwt.decode(
                current_jwt,
                key=current_app.config['SECRET_KEY']
            )
            print(current_jwt)

        if keep_logged_in:
            exp = iat + timedelta(seconds=app.config['JWT_MAX_EXPIRATION'])
        elif current_jwt and timedelta(seconds=current_jwt.get('duration')) > jwt_expiration_delta:
            exp = iat + timedelta(seconds=app.config['JWT_MAX_EXPIRATION'])
        else:
            exp = iat + jwt_expiration_delta

        return {
            'exp': exp,
            'iat': iat,
            'nbf': nbf,
            'identity': identity.public_id,
            'jwt_claim': str(identity.jwt_claim),
            'duration': int((exp - iat).total_seconds()),
        }

    @staticmethod
    def sign_jwt(_jwt):
        return jwt.encode(_jwt, current_app.config['SECRET_KEY'])
