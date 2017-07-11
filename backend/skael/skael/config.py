

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgres://postgres:@postgres/postgres'
    SECRET_KEY = 'test'
    MAILGUN_ORIGIN_DOMAIN = 'sandbox8a96f3c057b14e869059887391a8797e.mailgun.org'
    MAILGUN_ORIGIN_EMAIL = 'postmaster@sandbox8a96f3c057b14e869059887391a8797e.mailgun.org'
    MAILGUN_API_KEY = 'key-1c7814ed089d926cc10daf50b3bce91c'
    HOST = 'http://localhost:5000'
    JWT_MAX_EXPIRATION = 2592000
    VERIFY_EMAIL_CONTENT = """
<html>
<head>
    <title>Verify your account</title>
</head>
<body>
  Hello!

  <br>
  <br>
  Thanks for signing up, but first you need to verify your account.

  <br>
  <br>
  <form method="put" action="{0}">
    <button type="submit">Verify account</button>
  </form>

  <br>
  <br>
  Should the button above not work, copy the link below and paste it into your browser:

  <br>
  <br>
  <a href="{0}">{0}</a>
</body>
</html>
"""
    RESET_EMAIL_CONTENT = """
<html>
<head>
    <title>Reset your Password</title>
</head>
<body>
  To reset your password, click the button below

  <br>
  <br>
  <form method="put" action="{0}">
    <button type="submit">Reset password</button>
  </form>

  <br>
  <br>
  Should the button above not work, copy the link below and paste it into your browser:

  <br>
  <br>
  <a href="{0}">{0}</a>
</body>
"""



