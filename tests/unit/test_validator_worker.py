from unittest.mock import patch
from tests.test_base import BaseTest
from a55_api.validator_worker.main import validate_credit_request
from a55_api.validator_worker.validator import Validator
from a55_api.settings import MAX_AGE, MAX_AMOUNT


def fake_update_credit_request_status(ticket, status):
    # pylint: disable=unused-argument
    pass


class UtilsTest(BaseTest):
    def test_credit_request_is_valid(self):
        with patch("a55_api.validator_worker.main.update_credit_request_status",
                   wraps=fake_update_credit_request_status) as mock_update_status:

            ticket = 'any ticket string'
            status = validate_credit_request(
                MAX_AMOUNT, ticket, MAX_AGE, 0)

            self.assertEqual(status, "Approved")

            mock_update_status.assert_called_once_with(ticket, status)

    def test_credit_request_is_invalid(self):
        with patch("a55_api.validator_worker.main.update_credit_request_status",
                   wraps=fake_update_credit_request_status) as mock_update_status:

            ticket = 'any ticket string'
            status = validate_credit_request(
                MAX_AMOUNT + 1, ticket, MAX_AGE - 1, 0)

            self.assertEqual(status, "Denied")

            mock_update_status.assert_called_once_with(ticket, status)

    def test_credit_request_invalid_age(self):
        with patch("a55_api.validator_worker.main.update_credit_request_status",
                   wraps=fake_update_credit_request_status) as mock_update_status:

            ticket = 'any ticket string'
            status = validate_credit_request(
                MAX_AMOUNT, ticket, MAX_AGE - 1, 0)

            self.assertEqual(status, "Denied")

            mock_update_status.assert_called_once_with(ticket, status)

    def test_credit_request_invalid_amount(self):
        with patch("a55_api.validator_worker.main.update_credit_request_status",
                   wraps=fake_update_credit_request_status) as mock_update_status:

            ticket = 'any ticket string'
            status = validate_credit_request(
                MAX_AMOUNT + 1, ticket, MAX_AGE, 0)

            self.assertEqual(status, "Denied")

            mock_update_status.assert_called_once_with(ticket, status)

    def test_validator_returns_true(self):
        validator = Validator(MAX_AMOUNT, MAX_AGE)
        check_result = validator.validate()

        self.assertTrue(check_result)

    def test_validator_returns_false(self):
        validator = Validator(MAX_AMOUNT + 1, MAX_AGE - 1)
        check_result = validator.validate()

        self.assertFalse(check_result)
