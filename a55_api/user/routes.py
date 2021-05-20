from flask import Blueprint
from a55_api.user.controllers import show, index, create, update, delete

userBlueprint = Blueprint("user", __name__)

userBlueprint.route("/user", methods=["GET"])(index)
userBlueprint.route("/user", methods=["POST"])(create)
userBlueprint.route("/user/<user_id>", methods=["PUT"])(update)
userBlueprint.route("/user/<user_id>", methods=["DELETE"])(delete)
userBlueprint.route("/user/<user_id>", methods=["GET"])(show)
