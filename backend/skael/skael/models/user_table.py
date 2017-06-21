import uuid

import bcrypt

from skael.models import db, base_model


class UserTable(base_model.BaseTable):
    """
    Houses the DB definition of the users table.
    """
    __tablename__ = 'users'

    # Basic schema definition containing info pertinent to who the user is
    # as a member of the system.
    email = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Binary(64), nullable=False)
    username = db.Column(db.Text, nullable=False, unique=True)

    # House keeping stuff
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    is_validated = db.Column(db.Boolean, nullable=False, default=False)
    jwt_claim = db.Column(db.String(36), nullable=True, index=True)

    verify_token = db.Column(
        db.String(36),
        unique=True,
        nullable=True,
        index=True
    )

    reset_token = db.Column(
        db.String(36),
        unique=True,
        nullable=True,
        index=True
    )

    def __init__(self, email, plaintext_password, username):
        """
        Handles creation of the user object.

        :param str email: The user's email.
        :param str plaintext_password: The user's password in plaintext.
        :param str username: The user's desired username.
        """
        super().__init__()

        self.email = email
        self.password = self.bcrypt_password(plaintext_password)
        self.username = username
        self.verify_token = str(uuid.uuid4())

    def __repr__(self):
        """
        Define a log-safe string for the user table.

        :rtype: str
        :return: Returns log-safe definition of the model for better debugging.
        """
        return 'Email: {0} -- Deleted: {1} -- UUID: {2}'.format(
            self.email,
            self.is_deleted,
            self.public_id
        )

    def compare_password(self, plaintext_password):
        """
        Compares a user-input password to the stored hash.

        :param str plaintext_password: The password that the user put in.
        :rtype: bool
        :return: True if valid password--False otherwise.
        """
        if isinstance(self.password, bytes):
            return bcrypt.checkpw(
                plaintext_password.encode('utf-8'),
                self.password.decode('utf-8').encode('utf-8')
            )
        else:
            return bcrypt.checkpw(
                plaintext_password.encode('utf-8'),
                self.password.encode('utf-8')
            )

    @staticmethod
    def bcrypt_password(plaintext_password, work_factor=10):
        """
        Bcrypt hashes a password. Work factor of 10 is advised for production.

        :param str plaintext_password: The password to hash.
        :rtype: str
        :return: The bcrypt hash of the password.
        """
        return bcrypt.hashpw(
            plaintext_password.encode('utf-8'),
            bcrypt.gensalt(work_factor, b'2b')
        )

    @staticmethod
    def bcrypt_compare(plaintext, stored_password):
        """
        Handles comparing a password to the stored password.

        :param str plaintext:
        :param str stored_password: The password currently stored for the user.
        :rtype: bool
        :return: The outcome of if the password is correct.
        """
        return bcrypt.checkpw(plaintext.encode('utf-8'), stored_password)
