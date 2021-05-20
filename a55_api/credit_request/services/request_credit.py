from a55_api.credit_request.model import CreditRequest
from a55_api.user.repository import UserRepository

from a55_api.validator_worker.main import validate_credit_request

from a55_api.exceptions import A55ApiError


def request_credit(credit_request_data):
    user_external_id = credit_request_data["user_id"]

    user = UserRepository.get_by_external_id(user_external_id)

    if user is None:
        raise A55ApiError.user_not_found()

    payload = {
        "amount_required": credit_request_data["amount_required"],
        "user_id": user.id
    }

    credit_request = CreditRequest(**payload)
    credit_request.save()

    validator_data = {
        "amount": credit_request.amount_required,
        "ticket": credit_request.ticket,
        "age": user.age
    }
    validate_credit_request.delay(**validator_data)

    return credit_request
