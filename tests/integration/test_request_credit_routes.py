from unittest.mock import patch
import json
import logging
from tests.test_base import BaseTest


def fake_validate_credit_request(**kwargs):
    # pylint: disable=unused-argument
    pass


class RequestCreditRoutesTest(BaseTest):
    def setUp(self):
        logging.disable(logging.CRITICAL)

    def test_request_ticket(self):
        with patch("a55_api.validator_worker.main.validate_credit_request.delay",
                   wraps=fake_validate_credit_request):
            with self.flask_app.test_client() as client:
                user_payload = {
                    "name": "test",
                    "birth_date": "2001-01-01"
                }
                response = client.post(
                    "/user", data=json.dumps(user_payload), content_type="application/json")

                valid_user_id = response.json["id"]

                credit_request_payload = {
                    "amount_required": 5000,
                    "user_id": valid_user_id
                }
                response = client.post(
                    "/credit_request", data=json.dumps(credit_request_payload),
                    content_type="application/json")

                self.assertEqual(response.status_code, 200)
                ticket = response.json["ticket"]

                response = client.get(f"/credit_request/{ticket}")

                self.assertEqual(response.status_code, 200)

    def test_credit_payload_integrity(self):
        with self.flask_app.test_client() as client:
            wrong_payload = {
                "money": 5000
            }
            response = client.post(
                "/credit_request", data=json.dumps(wrong_payload), content_type="application/json")
            self.assertEqual(response.status_code, 400)

    def test_credit_payload_format(self):
        with self.flask_app.test_client() as client:
            wrong_payload = "some random text"

            response = client.post(
                "/credit_request", data=json.dumps(wrong_payload), content_type="application/json")
            self.assertEqual(response.status_code, 400)

    def test_credit_parameter_format(self):
        with self.flask_app.test_client() as client:
            ticket = "this is not a uuid"

            response = client.get(f"/credit_request/{ticket}")
            self.assertEqual(response.status_code, 400)

    def test_ticket_not_found(self):
        with self.flask_app.test_client() as client:
            ticket = "685dfe52-c7fb-4edd-be8d-4d8f11dcf2af"

            response = client.get(f"/credit_request/{ticket}")
            self.assertEqual(response.status_code, 404)
