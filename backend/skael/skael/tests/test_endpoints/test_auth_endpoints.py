from http import HTTPStatus
import unittest
import json

from skael.models import db
from skael.models.user_table import UserTable as User
from skael.DAOs.user_dao import UserDAO
from skael.utils.marshalizers import UserMarshal
from skael.utils.exceptions import IntegrationException

from skael.skael import create_app

app = create_app()


class TestUserAuthTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with app.app_context():
            db.drop_all()
            db.create_all()

            cls.test_client = app.test_client()
            cls.test_dao = UserDAO()

    def setUp(self):
        with app.app_context():
            test_user = User(
                'test@email.com',
                'testpw',
                'test-verify'
            )
            test_user.is_validated = True

            self.test_user_token = test_user.verify_token
            self.test_uid = test_user.public_id

            db.session.add(test_user)
            db.session.commit()

            data = {
                'username': test_user.username,
                'password': 'testpw'
            }

            response = self.test_client.post(
                '/auth',
                content_type='application/json',
                data=json.dumps(data)
            )

            response = json.loads(str(response.data.decode('utf-8')))
            self.access_token = response['access_token']

    def tearDown(self):
        with app.app_context():
            db.session.query(User).delete()
            db.session.commit()

    def test_get_verify_jwt(self):
        with app.app_context():
            response = self.test_client.get(
                '/users/auth',
                headers=dict(Authorization='Jwt {0}'.format(self.access_token))
            )

            self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_verify_jwt_fail_invalid_jwt(self):
        with app.app_context():
            response = self.test_client.get(
                '/users/auth',
                headers=dict(Authorization='Jwt {0}Z'.format(self.access_token))
            )

            self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
