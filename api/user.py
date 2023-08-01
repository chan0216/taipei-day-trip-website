import model.user
import jwt
import re
from flask import Blueprint, request, make_response
from decouple import config
from common.utils.error_util import EmailException
from common.utils.response_util import success,failure
from common.utils.request_util import check_request
from datetime import datetime,timedelta

user_blueprint = Blueprint('user', __name__)


#處理會員註冊
@user_blueprint.route("/user", methods=["POST"])
@check_request("name", "email", "password")
def signup_user():
    data = request.get_json()
    pattern = re.compile("^([\w\.\-]){1,64}\@([\w\.\-]){1,64}$")
    if not pattern.match(data['email']):
        return failure("Email格式錯誤", 400)
    try:
        result = model.user.user_signup(data)
        return success()
    except EmailException as e:
        return failure(str(e), 400)
    except Exception as e:
        return failure()

# 處理會員登入
@user_blueprint.route("/user", methods=["PATCH"])
@check_request("email", "password")
def signin_user():
    data = request.get_json()
    try:
        result = model.user.user_signin(data)
        if result:
            payload = {
                "user": result['email'],
                "user_id": result['id'],
                "exp": datetime.utcnow() + timedelta(days=7)
            }
            token = jwt.encode(payload, config(
                "secret_key"), algorithm='HS256')
            res = make_response(success())
            res.set_cookie('token', token, expires=datetime.utcnow(
            ) + timedelta(days=7))
            return res
        else:
            return failure("登入失敗，帳號或密碼錯誤", 400)
    except Exception as e:
        return failure(str(e),500)

#取得會員資料
@user_blueprint.route("/user", methods=["GET"])
def get_user():
    token = request.cookies.get('token')
    if token:
        data = jwt.decode(token.encode('UTF-8'),
                          config("secret_key"), algorithms=["HS256"])
        result = model.user.get_user(data)
        if result:
            return success(result)
        else:
            return success()
    else:
        return success()


@user_blueprint.route("/user", methods=["DELETE"])
def delete_user():
    res = make_response(success())
    res.set_cookie('token', expires=0)
    return res
