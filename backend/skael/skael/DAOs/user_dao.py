import logging
import uuid

from http import HTTPStatus
from sqlalchemy.exc import IntegrityError
from flask_jwt import current_identity

from skael.models import db
from skael.models.user_table import UserTable as User
from skael.utils.database_utils import exec_and_commit
from skael.utils.exceptions import DAOException


class UserDAO(object):
    """
    DAO object used to handle user management.
    """

    def get(self, user_id):
        """
        Retrieves a single user by its user id.

        :param str user_id: The User ID to look up.
        :rtype: UserTable
        :return: The UserTable row or None.
        """
        return db.session.query(
            User
        ).filter(
            User.public_id == str(user_id),
            User.is_deleted == False
        ).first()

    def get_by_username(self, username):
        """
        Handles retrieving a user by its username.

        :param str username: The username to fetch.
        :raises: DAOException
        :rtype: UserTable
        :return: The UserTable row or throws 404.
        """
        found_user = db.session.query(
            User
        ).filter_by(
            username=username
        ).first()

        if found_user is None:
            logging.error(
                'Failed to retrieve user by username: {0}'.format(username)
            )

            raise DAOException(
                'Requested user not found.',
                HTTPStatus.NOT_FOUND
            )

        return found_user

    def get_by_email(self, email):
        """
        Retrieves user info by the user's email.

        :param str email: The user to retrieve by email. Emails are unique so
        this is a safe retrieval.
        :rtype: UserTable
        :return: The UserTable row or None
        """
        return db.session.query(
            User
        ).filter_by(email=email).first()

    def get_by_token(self, token, *, is_verify_token=True):
        """
        Retrieves user info by the user's validation token.

        :param str token: The unique validation token for a user.
        :param bool is_verify_token: Toggles if we're fetching by
        `verify_token` or `reset_token`.
        :rtype: UserTable
        :raises: DAOException
        :return: The UserTable row.
        """
        found_user = db.session.query(
            User
        )

        if is_verify_token:
            found_user = found_user.filter_by(
                verify_token=token,
            ).first()
        else:
            found_user = found_user.filter_by(
                reset_token=token,
            ).first()

        if found_user is None:
            logging.error(
                'Failed to find requested account from token {0}.'
            )
            raise DAOException(
                'Failed to find user by validation token.',
                HTTPStatus.NOT_FOUND
            )

        return found_user

    def create_new_user(self, email, password, username, *, skip_commit=False):
        """
        Handles the creation of a new user.

        :param str email: The user's email to be registered with the account.
        :param str password: The desired password (not yet hashed).
        :param str username: The desired username for the user.
        :param bool skip_commit: An optional flag used to indicate if we want
        to create the object and add to DB delta, but not commit it just yet.
        Used mostly for facade methods which roll back if the event doesn't
        fully complete (transaction doesn't finalize, &c.).
        :rtype: UserTable
        :return: The newly created user table.
        """
        new_user = User(
            email,
            password,
            username
        )

        exec_and_commit(db.session.add, new_user, skip_commit=skip_commit)

        return new_user

    def logout_current_user(self):
        """
        Handles taking the currently authenticated JWT in the request,
        parsing out the user's public ID, and logging it out.

        :raises: DAOException
        """
        if current_identity is None:
            raise DAOException('User is not currently logged in.')

        db.session.query(
            User
        ).filter_by(
            public_id=current_identity.public_id
        ).update({
            'jwt_claim': None
        })

        db.session.commit()

    def update_user_data(self, user_id, **args):
        _update = {}

        current_user = None
        plaintext = args.get('plaintext_password')
        current_pass = args.get('current_password')
        if plaintext and plaintext != '':
            current_user = self.get(user_id)
            if current_user is None:
                logging.info(
                    'Attempted to update plaintext password for non-existent'
                    'account {0}'.format(user_id)
                )
                raise DAOException(
                    'Requested user to update does not exist.'
                )

        for k, v in args.items():
            if k == 'plaintext_password' and (v != '' or v is not None):
                if User.bcrypt_compare(current_pass, current_user.password):
                    _update['password'] = User.bcrypt_password(plaintext)

                    _update['jwt_claim'] = None
                    continue
                else:
                    raise DAOException('Invalid current password.')

            if k == 'current_password':
                continue

            _update[k] = v

        User.query.filter_by(public_id=str(user_id)).update(_update)
        db.session.commit()

        return self.get(user_id)

    def soft_delete(self, user_id):
        """
        Sets a "deleted" flag on the user.

        :param str user_id: The user to "delete".
        :rtype: Boolean
        :return: True if successful execution, exception otherwise.
        """
        User.query.filter_by(
            public_id=str(user_id)
        ).update({
            "is_deleted": True
        })
        db.session.commit()

        return True

    def verify_token(self, token):
        """
        Handles validating an account by its token.

        :param str token: The unique token to validate for.
        :rtype: UserTable
        :return: The validated user.
        """
        found_user = self.get_by_token(token)

        User.query.filter_by(
            public_id=found_user.public_id
        ).update({
            'is_validated': True,
            'verify_token': None,
        })

        db.session.commit()

        return self.get(found_user.public_id)

    def regenerate_token(self, email, token_choice):
        """
        Handles regenerating a  token for a user.

        :param str email: The user's email to regenerate for.
        :param str token_choice: `verify_token` or `reset_token`.
        :rtype: str
        :returns: The newly generated token.
        """
        found_user = self.get_by_email(email)

        if found_user is None:
            logging.error(
                'Failed to regenerate token for email {0}. '
                'Email not exists.'.format(email)
            )
            raise DAOException(
                'Failed to find requested user account.',
                HTTPStatus.NOT_FOUND
            )

        if found_user.is_validated and token_choice == 'verify_token':
            logging.error('Requested user {0} is already activated. Skipping.')
            raise DAOException('Requested account is already activated.')

        return self._regen_token(email, token_choice), found_user

    def reset_user_password(self, token, plaintext_password):
        """
        Handles resetting a user's password. If failure, throws a DAOException
        with a manual 404.

        :param str token: The user's reset token. Used to verify requesting
        user is who they say they are.
        :param str plaintext_password: The new password.
        :raises: DAOException
        """
        found_user = self.get_by_token(token, is_verify_token=False)

        db.session.query(
            User
        ).filter_by(
            public_id=found_user.public_id
        ).update({
            'password': User.bcrypt_password(plaintext_password),
            'reset_token': None,
            'jwt_claim': None
        })
        db.session.commit()

        return self.get(found_user.public_id)

    def _regen_token(self, email, token_choice):
        """
        Handles regenerating reset and user verification tokens.

        :param str email: The email to regenerate the password reset token for.
        :param str token_choice: `verify_token` or `reset_token`.
        :rtype: str
        :return: The newly generated token.
        """
        new_token = uuid.uuid4()

        try:
            db.session.query(
                User
            ).filter_by(
                email=email
            ).update({
                token_choice: new_token
            })
            db.session.commit()

            return new_token
        except IntegrityError:
            self._regen_token(email, token_choice)
