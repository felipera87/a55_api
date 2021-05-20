from flask import request
from flask_apispec import marshal_with
from marshmallow import ValidationError

from a55_api.exceptions import A55ApiError
from a55_api.utils import validate_uuid, log
from a55_api.user.services.update_user import update_user
from a55_api.user.services.create_new_user import create_new_user

from a55_api.user.repository import UserRepository
from a55_api.user.serializer import (user_schema,
                                     user_schemas,
                                     create_user_schema,
                                     update_user_schema)


@marshal_with(user_schema)
def show(user_id):
    log.info(f"Getting user {user_id}")

    if not validate_uuid(user_id):
        raise A55ApiError.invalid_uuid_parameter()

    user = UserRepository.get_by_external_id(user_id)

    if user is None:
        raise A55ApiError.user_not_found()

    log.info(f"Returning {user.__str__()}")
    return user


@marshal_with(user_schemas)
def index():
    log.info("Listing users")

    users = UserRepository.get_all_users()

    log.info(f"Returning list of {len(users)} users")
    return users


@marshal_with(user_schema)
def create():
    log.info("Creating user")

    if not request.json:
        raise A55ApiError.invalid_body_format()

    try:
        create_user_schema.load(request.json)
    except ValidationError as err:
        log.error(f"Validation errors: {err.messages}")
        raise A55ApiError.invalid_body_input()

    user_data = request.json
    user = create_new_user(user_data)

    log.info(f"Returning {user.__str__()}")
    return user


@marshal_with(user_schema)
def update(user_id):
    log.info(f"Updating user {user_id}")

    if not validate_uuid(user_id):
        raise A55ApiError.invalid_uuid_parameter()

    if not request.json:
        raise A55ApiError.invalid_body_format()

    try:
        update_user_schema.load(request.json)
    except ValidationError as err:
        log.error(f"Validation errors: {err.messages}")
        raise A55ApiError.invalid_body_input()

    user_data = request.json
    user = update_user(user_data, user_id)

    log.info(f"Returning {user.__str__()}")
    return user


def delete(user_id):
    log.info(f"Deleting user {user_id}")

    if not validate_uuid(user_id):
        raise A55ApiError.invalid_uuid_parameter()

    user = UserRepository.get_by_external_id(user_id)

    if user is None:
        raise A55ApiError.user_not_found()

    user.delete()

    log.info(f"Successfully deleted user {user_id}")
    return ""
