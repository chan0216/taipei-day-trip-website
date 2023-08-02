import jwt
from functools import wraps
from flask import request, jsonify
from flask import request, jsonify, make_response
from decouple import config

def check_request(*expected_args):  
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            json_object = request.get_json()
            if not json_object:
                return {"error": True, "message": "缺少請求參數"}, 400
            for expected_arg in expected_args:
                if expected_arg not in json_object:
                    return {"error": True, "message": f"請求缺少必要參數: {expected_arg}"}, 400
            return func(*args, **kwargs)
        return wrapper
    return decorator

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
