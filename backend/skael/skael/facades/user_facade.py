import logging

from flask import current_app

from skael.DAOs.user_dao import UserDAO
from skael.integrations.mailgun import MailgunIntegration
from skael.models import db
from skael.utils.exceptions import (
    IntegrationException,
    DAOException,
    FacadeException
)


class UserFacade(object):
    """
    Handles user operations which require multiple components.
    """

    def create_new_user(self, email, plaintext_password, username):
        """
        Handles creation of a new user and sending the verification token to
        the user.

        :param str email: The user's email
        :param str plaintext_password: The plaintext password. Is hashed
        at the model level.
        :param str username: The requested username for the user.
        :rtype: UserTable
        :return: The newly created user.
        """
        try:
            new_user = UserDAO().create_new_user(
                email,
                plaintext_password,
                username
            )

            MailgunIntegration().send_email(
                current_app.config['MAILGUN_ORIGIN_EMAIL'],
                new_user.email,
                'Please verify your account',
                current_app.config['VERIFY_EMAIL_CONTENT'].format(
                    '{0}/users/verify/{1}'.format(
                        current_app.config['HOST'],
                        new_user.verify_token,
                    )
                )
            )

            return new_user
        except IntegrationException as e:
            db.session.rollback()
            logging.error(
                'Failed to send mail when creating new user: {0}'.format(e)
            )

            raise FacadeException(
                'Failed to create user. Cannot send email.',
                e.status_code
            )
        except DAOException as e:
            db.session.rollback()
            logging.error(
                'Failed to create new user with exception: {0}'.format(e)
            )

            raise FacadeException(
                'Failed to create user. User creation failed.',
                e.status_code
            )
        finally:
            self._safe_commit()

    def regenerate_reset_password_token(self, email):
        """
        Regenerates a reset password token and sends another email.

        :param str email: The email of the user who forgot/lost their
        reset password email token.
        :rtype: str
        :return: The newly generated token.
        """
        try:
            new_token, user = UserDAO().regenerate_token(email, 'reset_token')

            MailgunIntegration().send_email(
                current_app.config['MAILGUN_ORIGIN_EMAIL'],
                user.email,
                'Reset your password',
                current_app.config['RESET_EMAIL_CONTENT'].format(
                    '{0}/users/reset_password/{1}'.format(
                        current_app.config['HOST'],
                        new_token,
                    )
                )
            )

            return new_token
        except IntegrationException as e:
            logging.error(
                'Failed to send email with exception: {0}'.format(
                    e
                )
            )

            raise FacadeException(
                'Failed to send reset token email.',
                e.status_code
            )
        except DAOException as e:
            logging.error(
                'Failed to regenerate reset token with exception: {0}'.format(
                    e
                )
            )

            raise FacadeException(
                'Failed to regenerate reset token.',
                e.status_code
            )

    def regenerate_verification_token(self, email):
        """
        Handles generating a new verification token should a user ever forget
        theirs.

        :param str email: The email of the user who forgot/lost their
        verification email.
        :rtype: str
        :return: The newly generated verification token.
        """

        try:
            new_token, user = UserDAO().regenerate_token(email, 'verify_token')

            MailgunIntegration.send_email(
                current_app.config['MAILGUN_ORIGIN_EMAIL'],
                user.email,
                'Please verify your account',
                current_app.config['VERIFY_EMAIL_CONTENT'].format(
                    new_token
                )
            )

            return new_token
        except IntegrationException as e:
            logging.error(
                'Failed to generate token for user with exception: {0}'.format(
                    e
                )
            )

            raise FacadeException(
                'Failed to generate new token. Email sending failed.',
                e.status_code
            )
        except DAOException as e:
            logging.error(
                'Failed to generate token for user with exception: {0}'.format(
                    e
                )
            )

            raise FacadeException(
                'Failed to generate new token: {0}'.format(e),
                e.status_code
            )

    def _safe_commit(self):
        try:
            db.session.commit()
        except IntegrationException as e:
            logging.info(
                'Failed to commit: {0}'.format(e)
            )

            raise FacadeException(
                'Failed to create new user.',
                e.status_code
            )

