from datetime import date
from tests.test_base import BaseTest

from a55_api.user.model import User


class UserTest(BaseTest):
    def test_user_model_create(self):
        birth_date = date(2001, 1, 1)
        payload = {
            "name": "test",
            "birth_date": birth_date
        }

        user = User(**payload)

        self.assertEqual(user.name, "test")
        self.assertEqual(user.birth_date, birth_date)

    def test_user_model_age_property(self):
        birth_date = date(2001, 1, 1)
        payload = {
            "name": "test",
            "birth_date": birth_date
        }

        user = User(**payload)
        check_age = date.today().year - birth_date.year

        self.assertEqual(user.age, check_age)
