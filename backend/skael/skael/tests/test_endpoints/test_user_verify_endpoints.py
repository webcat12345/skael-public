import unittest
import json
from http import HTTPStatus
from unittest import mock

from skael.DAOs.user_dao import UserDAO
from skael.skael import create_app
from skael.models import db
from skael.models.user_table import UserTable as User

app = create_app()


class VerificationEndpointsTestCase(unittest.TestCase):
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
                'test-verify@email.com',
                'testpw',
                'test-verify'
            )

            self.test_user_token = test_user.verify_token
            self.test_uid = test_user.public_id
            self.test_user_email = test_user.email

            db.session.add(test_user)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.query(
                User
            ).delete()
            db.session.commit()

    def test_token_verification(self):
        with app.app_context():
            data = {
                'token': self.test_user_token,
            }

            response = self.test_client.post(
                '/users/verify',
                content_type='application/json',
                data=json.dumps(data),
            )

            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertIsNotNone(response)

            found_user = UserDAO().get(self.test_uid)

            self.assertIsNotNone(found_user)
            self.assertIsNone(found_user.verify_token)
            self.assertTrue(found_user.is_validated)

    def test_token_verification_fail_invalid_token(self):
        with app.app_context():
            data = {
                'token': 'asldkfjalksdjf',
            }

            response = self.test_client.post(
                '/users/verify'.format(self.test_uid),
                content_type='application/json',
                data=json.dumps(data),
            )

            self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

            found_user = UserDAO().get(self.test_uid)

            self.assertIsNotNone(found_user)
            self.assertIsNotNone(found_user.verify_token)
            self.assertFalse(found_user.is_validated)

    @mock.patch('skael.integrations.mailgun.MailgunIntegration.send_email')
    def test_regenerate_token(self, mailgun_mock):
        mailgun_mock.return_value = None

        with app.app_context():
            found_user = UserDAO().get(self.test_uid)
            self.assertIsNotNone(found_user)
            original_token = found_user.verify_token

            data = {
                'email': self.test_user_email,
            }

            response = self.test_client.put(
                '/users/verify',
                content_type='application/json',
                data=json.dumps(data),
            )

            self.assertEqual(response.status_code, HTTPStatus.OK)

            found_user = UserDAO().get(self.test_uid)

            self.assertIsNotNone(found_user)
            self.assertIsNotNone(found_user.verify_token)
            self.assertNotEqual(found_user.verify_token, original_token)

    def test_regenerate_token_invalid_email(self):
        with app.app_context():
            data = {
                'email': 'INVALID EMAIL',
            }

            response = self.test_client.put(
                '/users/verify',
                content_type='application/json',
                data=json.dumps(data),
            )

            self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.drop_all()
