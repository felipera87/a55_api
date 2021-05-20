from unittest.mock import patch
from tests.test_base import BaseTest

from a55_api.validator_worker.db import update_credit_request_status
from a55_api.user.services.create_new_user import create_new_user
from a55_api.credit_request.services.request_credit import request_credit
from a55_api.credit_request.repository import CreditRequestRepository


def fake_validate_credit_request(**kwargs):
    # pylint: disable=unused-argument
    pass


class ValidatorWorkerTest(BaseTest):
    def test_change_status(self):
        with patch("a55_api.validator_worker.main.validate_credit_request.delay",
                   wraps=fake_validate_credit_request):

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
            ticket = credit_request.ticket

            self.assertEqual(credit_request.status, "In Progress")

            update_credit_request_status(ticket, "Approved")

            updated_credit_request = CreditRequestRepository.get_by_ticket(
                ticket)

            self.assertEqual(updated_credit_request.status, "Approved")
