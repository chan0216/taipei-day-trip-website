import json
import re
import model.order
import requests
import datetime
from decouple import config
from common.utils.request_util import token_required
from common.utils.response_util import success, failure
from flask import Blueprint, request

order_blueprint = Blueprint('order', __name__)

@order_blueprint.route("/order/<order_number>", methods=["GET"])
def get_order(order_number):
    try:
        result = model.order.get_order(order_number)
        if result:
            order_info = {
                "number": result["order_number"],
                "price": result["price"],
                "trip": {
                    "attraction": {
                        "id": result["attraction_id"],
                        "name": result["name"],
                        "address": result["address"],
                        "image": json.loads(result["images"])[0]
                    },
                    "date": result["date"],
                    "time": result["time_period"],
                },
                "contact": {
                    "name": result["name"],
                    "email": result["email"],
                    "phone": result["phone"]
                },
                "status": result["status"]
            }
            return success(order_info)
        else:
            return failure("沒有資料，請確認訂單編號",400)
    except Exception as e:
        return failure(e,500)



@order_blueprint.route("/orders", methods=["POST"])
@token_required
def post_order(current_user):
    data = request.get_json()
    try:
        name = data["order"]["contact"]["name"]
        email = data["order"]["contact"]["email"]
        phone_number = data["order"]["contact"]["phone"]
        email_pattern = re.compile(
            "[a-zA-Z0-9.-_]{1,}@[a-zA-Z.-]{2,}[.]{1}[a-zA-Z]{2,}")
        phone_pattern = re.compile("^(09)[0-9]{8}$")
        if not all([name, email, phone_number]):
            return failure("訂單建立失敗，欄位不得為空",400)
        elif not all([email_pattern.match(email), phone_pattern.match(phone_number)]):
            return failure("訂單建立失敗，電子郵件或電話格式不正確",400)
        else:
            order_number = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
            payload = {
                "prime": data["prime"],
                "partner_key": config('partner_key'),
                "merchant_id": "chan880216_CTBC",
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
            message='付款成功'
        else:
            message = "付款失敗"
        result = model.order.post_order(current_user,order_number, data, res['status'])
        if result:
            return success({"number": order_number, "payment": {"status": res["status"], "message": message}})
    except Exception as e:
        return failure()
