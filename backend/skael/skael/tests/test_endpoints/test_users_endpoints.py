import unittest
import json
import uuid
from http import HTTPStatus
from unittest import mock

from skael.models import db
from skael.models.user_table import UserTable as User
from skael.skael import create_app
from skael.DAOs.user_dao import UserDAO

app = create_app()


class TestUserRestPasswordTestCase(unittest.TestCase):
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
            if self.access_token is not None:
                self.test_client.delete(
                    '/users/logout',
                    headers=dict(
                        Authorization='Jwt {0}'.format(self.access_token)
                    )
                )

            db.session.query(User).delete()
            db.session.commit()

    def test_get_user(self):
        with app.app_context():
            response = self.test_client.get(
                '/users/{0}'.format(self.test_uid),
                headers=dict(Authorization='Jwt {0}'.format(self.access_token))
            )

            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertIsNotNone(response)

            response = json.loads(str(response.data.decode('utf-8')))
            self.assertEqual(response['email'], "test@email.com")

    def test_get_user_fail_user_not_exists(self):
        with app.app_context():
            response = self.test_client.get(
                '/users/{0}'.format(self.test_uid),
                headers=dict(Authorization='Jwt {0}'.format(self.access_token))
            )

            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertIsNotNone(response)

            response = json.loads(str(response.data.decode('utf-8')))
            self.assertEqual(response['email'], "test@email.com")

            self.assertIsNone(
                self.test_dao.get("9981ffba-2126-4afc-ad0b-49cfc29f98d9")
            )

    def test_get_user_fail_user_is_deleted(self):
        with app.app_context():
            response = self.test_client.get(
                '/users/{0}'.format(uuid.uuid4()),
                headers=dict(Authorization='Jwt {0}'.format(self.access_token))
            )

            self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_delete_user(self):
        with app.app_context():
            response = self.test_client.delete(
                '/users/{0}'.format(self.test_uid),
                headers=dict(Authorization='Jwt {0}'.format(self.access_token))
            )

            self.assertEqual(response.status_code, HTTPStatus.OK)

            deleted_user = db.session.query(User).filter_by(
                public_id=self.test_uid
            ).first()

            self.assertTrue(deleted_user.is_deleted)

    def test_delete_user_fail_user_not_exists(self):
        with app.app_context():
            response = self.test_client.delete(
                '/users/{0}'.format('1fe26e77-0c2c-41d3-b6a5-c352a7689131'),
                headers=dict(Authorization='Jwt {0}'.format(self.access_token))
            )

            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertIsNotNone(response)

            response = json.loads(str(response.data.decode('utf-8')))
            self.assertIsNone(response['email'])

    @mock.patch('skael.integrations.mailgun.MailgunIntegration.send_email')
    def test_create_user(self, send_email_mock):
        with app.app_context():
            send_email_mock.return_value = None

            data = {
                'email': 'testpostemail@testpostemail.com',
                'plaintext_password': 'testpw',
                'username': 'testpostemail'
            }

            response = self.test_client.post(
                '/users/'.format(self.test_uid),
                content_type='application/json',
                data=json.dumps(data),
            )

            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertIsNotNone(response)

            response = json.loads(str(response.data.decode('utf-8')))
            self.assertEqual(response['email'], data['email'])

            found_user = db.session.query(User).filter_by(
                public_id=response['public_id']
            ).first()

            self.assertIsNotNone(found_user)

    @mock.patch('skael.integrations.mailgun.MailgunIntegration.send_email')
    def test_create_user_fail_duplicate_email(self, mailgun_mock):
        mailgun_mock.return_value = None

        with app.app_context():
            data = {
                'email': 'test@email.com',
                'plaintext_password': 'testpw',
                'username': str(uuid.uuid4())
            }

            response = self.test_client.post(
                '/users/'.format(self.test_uid),
                content_type='application/json',
                data=json.dumps(data),
            )

            self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
            self.assertIsNotNone(response)

    @mock.patch('skael.integrations.mailgun.MailgunIntegration.send_email')
    def test_create_user_fail_duplicate_username(self, mailgun_mock):
        mailgun_mock.return_value = None

        with app.app_context():
            data = {
                'email': 'test@email.com',
                'plaintext_password': 'testpw',
                'username': 'test-verify'
            }

            response = self.test_client.post(
                '/users/'.format(self.test_uid),
                content_type='application/json',
                data=json.dumps(data),
            )

            self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
            self.assertIsNotNone(response)

            pass

    def test_put(self):
        with app.app_context():
            data = {
                'current_password': 'testpw',
                'plaintext_password': 'testnew-pass',
                'email': 'new_email@test.com',
            }

            response = self.test_client.put(
                '/users/{0}'.format(self.test_uid),
                content_type='application/json',
                data=json.dumps(data),
                headers=dict(Authorization='Jwt {0}'.format(self.access_token))
            )

            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertIsNotNone(response)

            user_info = db.session.query(User).filter_by(
                public_id=self.test_uid
            ).first()

            self.assertIsNotNone(user_info)

            self.assertEqual(user_info.email, 'new_email@test.com')
            self.assertTrue(
                User.bcrypt_compare(
                    data['plaintext_password'],
                    user_info.password
                )
            )

    def test_put_fail_duplicate_email(self):
        with app.app_context():
            pass

    def test_put_fail_duplicate_username(self):
        with app.app_context():

            pass

    def test_put_update_password_fail_invalid_current_password(self):
        with app.app_context():
            data = {
                'current_password': 'bad-password',
                'plaintext_password': 'test-pw'
            }

            response = self.test_client.put(
                '/users/{0}'.format(self.test_uid),
                content_type='application/json',
                data=json.dumps(data),
                headers=dict(Authorization='Jwt {0}'.format(self.access_token))
            )

            self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
            self.assertIsNotNone(response)

            response = json.loads(str(response.data.decode('utf-8')))
            self.assertEqual(
                response.get('msg'),
                'Invalid current password.'
            )

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.drop_all()
