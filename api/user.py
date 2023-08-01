import model.user
import jwt
import datetime
import re
from flask import Blueprint, request, jsonify, make_response
from decouple import config
from common.utils.error_util import EmailException
from common.utils.response_util import success,failure
from common.utils.request_util import check_request

user_blueprint = Blueprint('user', __name__)


#處理會員註冊
@user_blueprint.route("/user", methods=["POST"])
@check_request("name", "email", "password")
def signup_user():
    data = request.get_json()
    pattern = re.compile("^([\w\.\-]){1,64}\@([\w\.\-]){1,64}$")
    print(pattern.match(data['email']))
    if not pattern.match(data['email']):
        return failure("Email格式錯誤", 400)
    try:
        result = model.user.user_signup(data)
        return success()
    except EmailException as e:
        return failure(str(e), 400)
    except Exception as e:
        return failure()

# 登入會員
@user_blueprint.route("/user", methods=["PATCH"])
def user_signin():
    data = request.get_json()
    result = model.user.user_signin(data)
    if result is not None:
        payload = {
            "user": result['email'],
            "user_id": result["id"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=180)
        }
        token = jwt.encode(payload, config(
            "secret_key"), algorithm='HS256')
        res = make_response(jsonify({"ok": True}), 200)
        res.set_cookie('token', token, expires=datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=180))
        return res
    elif result == "error":
        res = make_response(
            jsonify({"error": True, "message": "伺服器內部錯誤"}), 500)
    else:
        res = make_response(
            jsonify({"error": True, "message": "登入失敗，帳號或密碼錯誤"}), 400)
        return res


@user_blueprint.route("/user", methods=["GET"])
def get_user():
    token = request.cookies.get('token')
    if token:
        data = jwt.decode(token.encode('UTF-8'),
                          config("secret_key"), algorithms=["HS256"])
        result = model.user.user_data(data)
        if result is not None:
            res = make_response(jsonify({"data": result}), 200)
            return res
        else:
            return jsonify({"data": None})
    else:
        return jsonify({"data": None})


@user_blueprint.route("/user", methods=["DELETE"])
def delete_user():
    res = make_response(jsonify({"ok": True}), 200)
    res.set_cookie('token', expires=0)
    return res
