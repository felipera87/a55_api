from tests.test_base import BaseTest

from a55_api.credit_request.model import CreditRequest


class CreditRequestTest(BaseTest):
    def test_credit_request_model_create(self):
        payload = {
            "amount_required": 5000,
            "user_id": "any user id"
        }

        credit_request = CreditRequest(**payload)

        self.assertEqual(credit_request.amount_required, 5000)
        self.assertEqual(credit_request.user_id, "any user id")
