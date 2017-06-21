

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgres://postgres:@postgres/postgres'
    SECRET_KEY = 'test'
    MAILGUN_ORIGIN_DOMAIN = 'sandbox8a96f3c057b14e869059887391a8797e.mailgun.org'
    MAILGUN_ORIGIN_EMAIL = 'postmaster@sandbox8a96f3c057b14e869059887391a8797e.mailgun.org'
    MAILGUN_API_KEY = 'key-1c7814ed089d926cc10daf50b3bce91c'
    VERIFY_EMAIL_CONTENT = 'Your account verification token: {0}'
    RESET_EMAIL_CONTENT = 'Your password reset token: {0}'
