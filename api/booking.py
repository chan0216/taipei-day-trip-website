import model.booking
from common.utils.request_util import token_required, check_request
from common.utils.response_util import success, failure
from flask import Blueprint, request

booking_blueprint = Blueprint('booking', __name__)

@booking_blueprint.route("/booking", methods=["GET"])
@token_required
def get_booking(current_user):
    try:
        result = model.booking.get_booking(current_user)
        if not result:
            return success()
        else:
            booking_info = {
                "attraction": {
                "id": result["id"],
                "name": result["name"],
                "address": result["address"],
                "image": result["images"][0]
                },
                "date": result["date"],
                "time": result["time_period"],
                "price": result["price"]
            }
            return success(booking_info)
    except Exception as e:
        return failure()


@booking_blueprint.route("/booking", methods=["POST"])
@token_required
@check_request("attractionId", "date", "time", "price")
def post_booking(current_user):
    try:
        data = request.get_json()
        result = model.booking.post_booking(data, current_user)
        return success()
    except ValueError as e:
        return failure("建立失敗，輸入不正確",400)
    except Exception as e:
        return failure()


@booking_blueprint.route("/booking", methods=["DELETE"])
@token_required
def handle_delete(current_user):
    try:
        result = model.booking.delete_booking(current_user)
        return success()
    except Exception as e:
        return failure()
