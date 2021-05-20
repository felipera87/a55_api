from flask import jsonify
from a55_api.utils import log


class A55ApiError(Exception):
    status_code = 500

    def __init__(self, message, error_type, status_code=None):
        Exception.__init__(self)

        self.message = message
        self.error_type = error_type

        if status_code is not None:
            self.status_code = status_code

    def to_json(self):
        log.error(
            f"A55ApiError: {self.error_type}, {self.status_code}, {self.message}")
        return jsonify({"error": self.error_type, "message": self.message})

    @classmethod
    def user_not_found(cls):
        error = {
            "error_type": "user_not_found",
            "message": "The user id was not found on our database.",
            "status_code": 404
        }
        return cls(**error)

    @classmethod
    def ticket_not_found(cls):
        error = {
            "error_type": "ticket_not_found",
            "message": "Your ticket was not found on our database.",
            "status_code": 404
        }
        return cls(**error)

    @classmethod
    def invalid_body_format(cls):
        error = {
            "error_type": "invalid_body_format",
            "message": "The request body couldn't be parsed, make sure it is a valid JSON.",
            "status_code": 400
        }
        return cls(**error)

    @classmethod
    def invalid_body_input(cls):
        error = {
            "error_type": "invalid_body_input",
            "message": "The request body is invalid. Check required fields, names and formats.",
            "status_code": 400
        }
        return cls(**error)

    @classmethod
    def invalid_uuid_parameter(cls):
        error = {
            "error_type": "invalid_uuid_parameter",
            "message": "The parameter is not a valid UUID.",
            "status_code": 400
        }
        return cls(**error)


def generic_bad_request(error_msg):
    print(error_msg)
    error = {
        "error": "bad_request",
        "message": "Something went wrong handling user input, check your parameters/payloads."
    }
    return error, 400


def generic_system_error(error_msg):
    print(error_msg)
    error = {
        "error": "system_error",
        "message": "Something went wrong on our servers."
    }
    return error, 500
