from functools import wraps
from flask import request, jsonify

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