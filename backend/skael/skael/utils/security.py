import uuid

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

