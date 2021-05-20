from unittest.mock import patch
from tests.test_base import BaseTest

from a55_api.user.services.create_new_user import create_new_user
from a55_api.credit_request.services.request_credit import request_credit


def fake_validate_credit_request(**kwargs):
    # pylint: disable=unused-argument
    pass


class CreditRequestTest(BaseTest):
    def test_request_credit(self):
        with patch("a55_api.validator_worker.main.validate_credit_request.delay",
                   wraps=fake_validate_credit_request) as mock_validate_credit_request:

            user_payload = {
                "name": "test",
                "birth_date": "2001-01-01"
            }

            user = create_new_user(user_payload)

            request_credit_payload = {
                "amount_required": 5000,
                "user_id": user.external_id
            }

            credit_request = request_credit(request_credit_payload)

            mock_validate_credit_request.assert_called_once_with(
                amount=credit_request.amount_required,
                ticket=credit_request.ticket,
                age=user.age
            )

            self.assertIsNotNone(credit_request.id)
            self.assertIsNotNone(credit_request.ticket)
            self.assertEqual(credit_request.amount_required, 5000)
            self.assertEqual(credit_request.user_id, user.id)
            self.assertEqual(credit_request.status, "In Progress")
            self.assertIsNotNone(credit_request.created_at)
            self.assertIsNotNone(credit_request.updated_at)
