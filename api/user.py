from flask import Blueprint,request,jsonify,make_response,session
from model.public import con_pool
from decouple import config
import jwt
import datetime

import re
user_blueprint = Blueprint('user', __name__)
db=con_pool.get_connection()
cursor=db.cursor(dictionary=True,buffered=True)
#處理註冊會員
@user_blueprint.route("/user",methods=["POST"])
def signup_user():
    try:
        data = request.get_json()
        name=data["name"]
        email=data["email"]
        password=data["password"]
        cursor.execute("SELECT email FROM user WHERE email=%s", (email,))
        userEmail=cursor.fetchone()
        pattern=re.compile("^([\w\.\-]){1,64}\@([\w\.\-]){1,64}$")
        if userEmail is None:
            if pattern.match(email):
                cursor.execute("INSERT INTO user (name, email, password) VALUES (%s, %s, %s)",
                (name,email,password))
                db.commit()
                res = make_response(jsonify({"ok": True}), 200)
                return res
        else: 
            res = make_response(jsonify({"error": True,"message": "註冊失敗,重複的Email"}), 400)
            return res
 
    except:
        res = make_response(jsonify({"error": True,"message": "伺服器內部錯誤"}),500)
        return res
#登入會員
@user_blueprint.route("/user",methods=["PATCH"])
def login_user():
    try:
        data = request.get_json()
        email=data["email"]
        password=data["password"]
        cursor.execute("SELECT name,email,password FROM user WHERE email=%s and password=%s", (email,password))
        userData=cursor.fetchone()
        if userData is not None:
            # session["email"]=userData["email"]
            payload={
                "user":userData['email'],
                "exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=180)

            }
            token=jwt.encode(payload,config("secret_key"), algorithm='HS256')
            res = make_response(jsonify({"ok": True}), 200)
            res.set_cookie('token',token,expires=datetime.datetime.utcnow() + datetime.timedelta(minutes=180))
            return res
        else: 
            res = make_response(jsonify({"error": True,"message": "登入失敗，帳號或密碼錯誤"}), 400)
            return res
    except:
            res = make_response(jsonify({"error": True,"message": "伺服器內部錯誤"}),500)
            return res

@user_blueprint.route("/user",methods=["GET"])
def getUser():
    token=request.cookies.get('token')
    if token is not None:
        data=jwt.decode(token.encode('UTF-8'), config("secret_key"), algorithms=["HS256"])
        cursor.execute("SELECT id,name,email FROM user WHERE email=%s", (data["user"],))
        userData=cursor.fetchone()
        res = make_response(jsonify({"data": userData}),200)
        return res
    else:
        return jsonify({"data":None})

@user_blueprint.route("/user",methods=["DELETE"])
def deleteUser():
    res=make_response(jsonify({"ok": True}),200)
    # res.delete_cookie("token")
    res.set_cookie('token', expires=0)
    return res

