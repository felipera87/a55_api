from flask import request
from flask_apispec import marshal_with
from marshmallow import ValidationError

from a55_api.utils import validate_uuid, log
from a55_api.exceptions import A55ApiError
from a55_api.credit_request.services.request_credit import request_credit
from a55_api.credit_request.repository import CreditRequestRepository

from a55_api.credit_request.serializer import (credit_request_schema,
                                               credit_request_schemas,
                                               create_credit_request_schema)


@marshal_with(credit_request_schema)
def show(ticket):
    log.info(f"Getting ticket {ticket}")

    if not validate_uuid(ticket):
        raise A55ApiError.invalid_uuid_parameter()

    credit_request = CreditRequestRepository.get_by_ticket(ticket)

    if credit_request is None:
        raise A55ApiError.ticket_not_found()

    log.info(f"Returning {credit_request.__str__()}")
    return credit_request


@marshal_with(credit_request_schemas)
def index():
    log.info("Listing credit requests")

    credit_requests = CreditRequestRepository.get_all_requests()

    log.info(f"Returning list of {len(credit_requests)} credit requests")
    return credit_requests


@marshal_with(credit_request_schema)
def create():
    log.info("Requesting credit")

    if not request.json:
        raise A55ApiError.invalid_body_format()

    try:
        create_credit_request_schema.load(request.json)
    except ValidationError as err:
        log.error(f"Validation errors: {err.messages}")
        raise A55ApiError.invalid_body_input()

    credit_request_data = request.json
    credit_request = request_credit(credit_request_data)

    log.info(f"Returning {credit_request.__str__()}")
    return credit_request
