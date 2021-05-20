import json
import logging
from tests.test_base import BaseTest


class UserRoutesTest(BaseTest):
    def setUp(self):
        logging.disable(logging.CRITICAL)

    def test_create_user(self):
        with self.flask_app.test_client() as client:
            payload = {
                "name": "test",
                "birth_date": "2001-01-01"
            }
            response = client.post(
                "/user", data=json.dumps(payload), content_type="application/json")

            self.assertEqual(response.status_code, 200)
            user_id = response.json["id"]

            response = client.get(f"/user/{user_id}")

            self.assertEqual(response.status_code, 200)

    def test_update_user(self):
        with self.flask_app.test_client() as client:
            payload = {
                "name": "test",
                "birth_date": "2001-01-01"
            }
            response = client.post(
                "/user", data=json.dumps(payload), content_type="application/json")

            user_id = response.json["id"]

            payload["name"] = "test2"
            response = client.put(
                f"/user/{user_id}", data=json.dumps(payload), content_type="application/json")
            self.assertEqual(response.status_code, 200)

            response = client.get(f"/user/{user_id}")

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json["name"], "test2")

    def test_delete_user(self):
        with self.flask_app.test_client() as client:
            payload = {
                "name": "test",
                "birth_date": "2001-01-01"
            }
            response = client.post(
                "/user", data=json.dumps(payload), content_type="application/json")

            user_id = response.json["id"]

            response = client.delete(f"/user/{user_id}")
            self.assertEqual(response.status_code, 200)

            response = client.get(f"/user/{user_id}")

            self.assertEqual(response.status_code, 404)

    def test_user_payload_integrity(self):
        with self.flask_app.test_client() as client:
            payload = {
                "name": "test",
                "birth_date": "2001-01-01"
            }
            response = client.post(
                "/user", data=json.dumps(payload), content_type="application/json")

            user_id = response.json["id"]

            wrong_payload = {
                "nameee": "test",
                "birth_date": "2001-01-01",
            }

            response = client.post(
                "/user", data=json.dumps(wrong_payload), content_type="application/json")
            self.assertEqual(response.status_code, 400)

            response = client.put(
                f"/user/{user_id}", data=json.dumps(wrong_payload), content_type="application/json")
            self.assertEqual(response.status_code, 400)

    def test_user_payload_format(self):
        with self.flask_app.test_client() as client:
            payload = {
                "name": "test",
                "birth_date": "2001-01-01"
            }
            response = client.post(
                "/user", data=json.dumps(payload), content_type="application/json")

            user_id = response.json["id"]

            wrong_payload = "some random text"

            response = client.post(
                "/user", data=json.dumps(wrong_payload), content_type="application/json")
            self.assertEqual(response.status_code, 400)

            response = client.put(
                f"/user/{user_id}", data=json.dumps(wrong_payload), content_type="application/json")
            self.assertEqual(response.status_code, 400)

    def test_user_parameter_format(self):
        with self.flask_app.test_client() as client:
            user_id = "this is not a uuid"

            payload = {
                "name": "test",
                "birth_date": "2001-01-01"
            }

            response = client.put(
                f"/user/{user_id}", data=json.dumps(payload), content_type="application/json")
            self.assertEqual(response.status_code, 400)

            response = client.delete(f"/user/{user_id}")
            self.assertEqual(response.status_code, 400)

            response = client.get(f"/user/{user_id}")
            self.assertEqual(response.status_code, 400)

    def test_user_not_found(self):
        with self.flask_app.test_client() as client:
            user_id = "685dfe52-c7fb-4edd-be8d-4d8f11dcf2af"

            payload = {
                "name": "test",
                "birth_date": "2001-01-01"
            }

            response = client.put(
                f"/user/{user_id}", data=json.dumps(payload), content_type="application/json")
            self.assertEqual(response.status_code, 404)

            response = client.delete(f"/user/{user_id}")
            self.assertEqual(response.status_code, 404)

            response = client.get(f"/user/{user_id}")
            self.assertEqual(response.status_code, 404)
