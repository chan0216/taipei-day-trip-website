import json
import re
import model.order
import requests
import datetime
from decouple import config
from common.utils.request_util import token_required
from flask import Blueprint, request, jsonify, make_response
order_blueprint = Blueprint('order', __name__)

@order_blueprint.route("/order/<orderNumber>", methods=["GET"])
def get_order(orderNumber):
    result = model.order.get_order(orderNumber)
    if result is not None:
        order_info = {
            "number": result["ordernumber"],
            "price": result["price"],
            "trip": {
                "attraction": {
                    "id": result["attraction_id"],
                    "name": result["name"],
                    "address": result["address"],
                    "image": json.loads(result["images"])[0]
                },
                "date": result["date"],
                "time": result["time"],
            },
            "contact": {
                "name": result["username"],
                "email": result["email"],
                "phone": result["phone"]
            },
            "status": result["status"]
        }
        return jsonify({"data": order_info})
    else:
        res = make_response(
            jsonify({"data": None, "message": "沒有資料，請確認訂單編號"}), 200)
        return res


@order_blueprint.route("/orders", methods=["POST"])
@token_required
def post_order(current_user):
    data = request.get_json()
    try:
        data = request.get_json()
        name = data["order"]["contact"]["name"]
        email = data["order"]["contact"]["email"]
        phone_number = data["order"]["contact"]["phone"]
        email_pattern = re.compile(
            "[a-zA-Z0-9.-_]{1,}@[a-zA-Z.-]{2,}[.]{1}[a-zA-Z]{2,}")
        phone_pattern = re.compile("^(09)[0-9]{8}$")
        if len(name) == 0 or len(email) == 0 or len(phone_number) == 0 or phone_pattern.match(phone_number) is None or email_pattern.match(email) is None:
            res = make_response(
                jsonify({"error": True, "message": "訂單建立失敗，輸入不完整或是格式不正確"}), 400)
            return res
        else:
            order_number = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
            payload = {
                "prime": data["prime"],
                "partner_key": config('partner_key'),
                "merchant_id": "chan880216_TAISHIN",
                "details": "TapPay Test",
                "amount": data["order"]["price"],
                "order_number": order_number,
                "cardholder": {
                    "phone_number": phone_number,
                    "name": name,
                    "email": email
                },
                "remember": True
            }
        headers = {'content-type': 'application/json',
                   "x-api-key": config('partner_key')}
        r = requests.post('https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime',
                          data=json.dumps(payload), headers=headers)
        res = r.json()
        if res["status"] == 0:
            message = "付款成功"
        else:
            message = "付款失敗"
        result = model.order.post_order(
            order_number, data, current_user, name, email, phone_number, res, message)
        return result
    except:
        res = make_response(
            jsonify({"error": True, "message": "伺服器內部錯誤"}), 500)
        return res
