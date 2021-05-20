from datetime import datetime
from a55_api.user.repository import UserRepository

from a55_api.exceptions import A55ApiError


def update_user(user_data, user_id):
    payload = {
        "name": user_data["name"],
        "birth_date": datetime.fromisoformat(user_data["birth_date"])
    }

    user = UserRepository.get_by_external_id(user_id)

    if user is None:
        raise A55ApiError.user_not_found()

    for key, value in payload.items():
        setattr(user, key, value)
    user.save()

    return user
