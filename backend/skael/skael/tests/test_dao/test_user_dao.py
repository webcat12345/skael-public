import unittest
import uuid

from skael.DAOs.user_dao import UserDAO
from skael.skael import create_app
from skael.models import db
from skael.models.user_table import UserTable as User
from skael.utils.exceptions import DAOException

app = create_app()


class UserDAOTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with app.app_context():
            db.drop_all()
            db.create_all()

            cls.test_dao = UserDAO()

            test_user = User(
                'test@email.com',
                'testpw',
                'test-{0}-username'.format(uuid.uuid4())
            )

            deleted_user = User(
                'delete-test@email.com',
                'testpassword',
                'test-{0}-username'.format(uuid.uuid4())
            )
            deleted_user.is_deleted = True

            user_to_delete = User(
                'user-to-delete@email.com',
                'testpw',
                'test-{0}-username'.format(uuid.uuid4())
            )

            cls.test_uid = test_user.public_id
            cls.deleted_uid = deleted_user.public_id
            cls.to_delete_uid = user_to_delete.public_id

            db.session.add(test_user)
            db.session.add(deleted_user)
            db.session.add(user_to_delete)
            db.session.commit()

    def test_get_pass(self):
        with app.app_context():
            response = self.test_dao.get(self.test_uid)
            self.assertIsNotNone(response)
            self.assertEqual(response.email, 'test@email.com')

    def test_get_fail_invalid_user_id(self):
        with app.app_context():
            self.assertIsNone(
                self.test_dao.get('9981ffba-2126-4afc-ad0b-49cfc29f98d9')
            )

    def test_get_fail_deleted_account(self):
        with app.app_context():
            self.assertIsNone(
                self.test_dao.get(self.deleted_uid)
            )

    def test_post(self):
        with app.app_context():
            new_user = self.test_dao.create_new_user(
                'test1@email.com',
                'testpw',
                'test-{0}-username'.format(uuid.uuid4())
            )

            self.assertIsNotNone(new_user)
            self.assertEqual(new_user.email, 'test1@email.com')

    def test_post_fail_duplicate_email(self):
        with self.assertRaises(DAOException):
            with app.app_context():
                self.test_dao.create_new_user(
                    'test1@email.com',
                    'testpw',
                    'test-{0}-username'.format(uuid.uuid4())
                )

    def test_delete(self):
        with app.app_context():
            response = self.test_dao.soft_delete(self.to_delete_uid)

            self.assertTrue(response)

            deleted_user = db.session.query(User).filter_by(
                public_id=self.to_delete_uid
            ).first()

            self.assertTrue(deleted_user.is_deleted)

    def test_delete_fail_nonexistent_user(self):
        with app.app_context():
            response = self.test_dao.soft_delete(
                '9981ffba-2126-4afc-ad0b-49cfc29f98d9'
            )

            self.assertTrue(response)

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.drop_all()
