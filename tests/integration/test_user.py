from tests.test_base import BaseTest

from a55_api.user.repository import UserRepository
from a55_api.user.services.create_new_user import create_new_user
from a55_api.user.services.update_user import update_user


class UserTest(BaseTest):
    def test_create_user(self):
        payload = {
            "name": "test",
            "birth_date": "2001-01-01"
        }

        user = create_new_user(payload)

        find_user = UserRepository.get_by_external_id(user.external_id)

        self.assertEqual(user.id, find_user.id)
        self.assertIsNotNone(find_user.created_at)
        self.assertIsNotNone(find_user.updated_at)
        self.assertIsNotNone(find_user.external_id)

    def test_update_user(self):
        payload = {
            "name": "test",
            "birth_date": "2001-01-01"
        }

        user = create_new_user(payload)

        created_user_values = {
            "id": user.id,
            "name": user.name,
            "updated_at": user.updated_at
        }

        payload["name"] = "test2"
        user = update_user(payload, user.external_id)

        self.assertEqual(user.id, created_user_values["id"])
        self.assertNotEqual(user.name, created_user_values["name"])
        self.assertEqual(user.name, "test2")
        self.assertNotEqual(user.updated_at, created_user_values["updated_at"])
