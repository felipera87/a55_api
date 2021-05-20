from datetime import datetime
from a55_api.user.model import User


def create_new_user(user_data):
    payload = {
        "name": user_data["name"],
        "birth_date": datetime.fromisoformat(user_data["birth_date"])
    }

    user = User(**payload)
    user.save()

    return user
