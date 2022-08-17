import jwt
import json
from functools import wraps
from decouple import config
from flask import Blueprint, request, jsonify, make_response
import model.booking
booking_blueprint = Blueprint('booking', __name__)


def token_required(f):
    @wraps(f)
    def decorated():
        token = request.cookies.get('token')
        if not token:
            res = make_response(
                jsonify({"error": True, "message": "未登入系統，拒絕存取"}), 403)
            return res
        try:
            jwtdata = jwt.decode(token.encode('UTF-8'),
                                 config("secret_key"), algorithms=["HS256"])
            current_user = jwtdata["user_id"]
        except Exception as e:
            res = make_response(
                jsonify({"error": True, "message": "伺服器內部錯誤"}), 500)
            return res
        return f(current_user)
    return decorated


@booking_blueprint.route("/booking", methods=["GET"])
@token_required
def handle_get(current_user):
    result = model.booking.get_booking(current_user)
    if result is None:
        return jsonify({"data": None})
    else:
        result["images"] = json.loads(result["images"])
        booking_info = {"attraction": {
            "id": result["id"],
            "name": result["name"],
            "address": result["address"],
            "image": result["images"][0]},
            "date": result["date"],
            "time": result["time"],
            "price": result["price"]
        }
        return jsonify({"data": booking_info})


@booking_blueprint.route("/booking", methods=["POST"])
@token_required
def handle_post(current_user):
    data = request.get_json()
    result = model.booking.post_booking(data, current_user)
    if result == "ok":
        res = make_response(jsonify({"ok": True}), 200)
    elif result == "error":
        res = make_response(
            jsonify({"error": True, "message": "伺服器內部錯誤"}), 500)
    else:
        res = make_response(
            jsonify({"error": True, "message": "建立失敗，輸入不正確"}), 400)
    return res


@booking_blueprint.route("/booking", methods=["DELETE"])
@token_required
def handle_delete(current_user):
    result = model.booking.delete_booking(current_user)
    if result == "ok":
        res = make_response(jsonify({"ok": True}), 200)
        return res
