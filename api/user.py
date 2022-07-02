from flask import Blueprint, request, jsonify, make_response
from model.public import con_pool
from decouple import config
import jwt
import datetime
import re
user_blueprint = Blueprint('user', __name__)
# 處理註冊會員


@user_blueprint.route("/user", methods=["POST"])
def signup_user():
    data = request.get_json()
    result = UserModel.user_signup(data)
    return UserView.render_signup(result)

# 登入會員


@user_blueprint.route("/user", methods=["PATCH"])
def login_user():
    data = request.get_json()
    result = UserModel.user_signin(data)
    return UserView.render_signin(result)


@user_blueprint.route("/user", methods=["GET"])
def get_user():
    result = UserModel.user_data()
    return UserView.render_userdata(result)


@user_blueprint.route("/user", methods=["DELETE"])
def delete_user():
    res = make_response(jsonify({"ok": True}), 200)
    # res.delete_cookie("token")
    res.set_cookie('token', expires=0)
    return res


class UserModel:
    def user_signup(self, data):
        try:
            db = con_pool.get_connection()
            cursor = db.cursor(dictionary=True, buffered=True)
            name = data["name"]
            email = data["email"]
            password = data["password"]
            cursor.execute("SELECT email FROM user WHERE email=%s", (email,))
            userEmail = cursor.fetchone()
            pattern = re.compile("^([\w\.\-]){1,64}\@([\w\.\-]){1,64}$")
            if userEmail is None:
                if pattern.match(email):
                    cursor.execute("INSERT INTO user (name, email, password) VALUES (%s, %s, %s)",
                                   (name, email, password))
                    return "ok"
            else:
                return "重複的Email"
        except:
            db.rollback()
            return "error"
        finally:
            cursor.close()
            db.commit()
            db.close()

    def user_signin(self, data):
        try:

            email = data["email"]
            password = data["password"]
            db = con_pool.get_connection()
            cursor = db.cursor(dictionary=True, buffered=True)
            cursor.execute(
                "SELECT name,email,password FROM user WHERE email=%s and password=%s", (email, password))
            userData = cursor.fetchone()
            return userData
        except:
            return "error"
        finally:
            cursor.close()
            db.close()

    def user_data(self):
        token = request.cookies.get('token')
        if token is not None:
            try:
                db = con_pool.get_connection()
                cursor = db.cursor(dictionary=True, buffered=True)
                data = jwt.decode(token.encode('UTF-8'),
                                  config("secret_key"), algorithms=["HS256"])
                cursor.execute(
                    "SELECT id,name,email FROM user WHERE email=%s", (data["user"],))
                userData = cursor.fetchone()
                return userData
            finally:
                db.close()


UserModel = UserModel()


class UserView:
    def render_signup(self, result):
        if result == "ok":
            res = make_response(jsonify({"ok": True}), 200)
            return res
        elif result == "error":
            res = make_response(
                jsonify({"error": True, "message": "伺服器內部錯誤"}), 500)
            return res
        else:
            res = make_response(
                jsonify({"error": True, "message": "註冊失敗,重複的Email"}), 400)
            return res

    def render_signin(self, result):
        if result is not None:
            payload = {
                "user": result['email'],
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

    def render_userdata(self, result):
        if result is not None:
            res = make_response(jsonify({"data": result}), 200)
            return res
        else:
            return jsonify({"data": None})


UserView = UserView()
