from flask import Blueprint
from a55_api.credit_request.controllers import show, index, create

creditRequestBlueprint = Blueprint("credit_request", __name__)

creditRequestBlueprint.route("/credit_request", methods=["GET"])(index)
creditRequestBlueprint.route("/credit_request", methods=["POST"])(create)
creditRequestBlueprint.route("/credit_request/<ticket>", methods=["GET"])(show)
