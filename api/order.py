import json
import re
import jwt
from decouple import config
from itsdangerous import NoneAlgorithm
import requests
import datetime
from flask import Blueprint,request,jsonify,make_response,session
from model.public import con_pool
order_blueprint = Blueprint('order', __name__)
@order_blueprint.route("/orders",methods=["POST"])
def handle_order():
  try:
      token=request.cookies.get('token')
      jwtdata=jwt.decode(token.encode('UTF-8'), config("secret_key"), algorithms=["HS256"])
      if token is None:
          res = make_response(jsonify({"error": True,"message": "未登入系統，拒絕存取"}), 403)
          return res
      
      data = request.get_json()
      name=data["order"]["contact"]["name"]
      email=data["order"]["contact"]["email"]
      phone_number=data["order"]["contact"]["phone"]
      email_pattern=re.compile("[a-zA-Z0-9.-_]{1,}@[a-zA-Z.-]{2,}[.]{1}[a-zA-Z]{2,}")
      phone_pattern=re.compile("^(09)[0-9]{8}$")
      if  len(name)==0 or len(email)==0 or len(phone_number)==0 or phone_pattern.match(phone_number) is None or email_pattern.match(email) is None:
          res = make_response(jsonify({"error": True,"message": "訂單建立失敗，輸入不完整或是格式不正確"}), 400)
          return res
      else:
        order_number=datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
        session[order_number]="未付款"
        payload={
        "prime": data["prime"],
        "partner_key": config('partner_key'),
        "merchant_id": "chan880216_TAISHIN",
          "details":"TapPay Test",
          "amount": data["order"]["price"],
          "order_number":order_number,
          "cardholder": {
            "phone_number": phone_number,
            "name": name,
            "email": email
        },
      "remember": True
      }
      headers = {'content-type': 'application/json', "x-api-key":config('partner_key')}
      r = requests.post('https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime', data=json.dumps(payload),headers=headers)
      res=r.json()
      if res["status"]==0:
        session[order_number]="已付款"
        message="付款成功"
      else:
        message="付款失敗"
      db=con_pool.get_connection()
      cursor=db.cursor(dictionary=True)
      sql = "Insert Into orders(ordernumber, price, username, email, phone, date, time, attractionId,status) Values( %s, %s, %s, %s, %s, %s, %s, %s,%s)"
      val=(order_number,data["order"]["price"],name,email,phone_number,data["order"]["trip"]["date"],data["order"]["trip"]["time"],data["order"]["trip"]["attraction"]["id"],res["status"])
      cursor.execute(sql, val)
      db.commit()
      cursor.execute("DELETE FROM schedule WHERE email=%s",(jwtdata["user"],))
      db.commit()
      db.close()
      return jsonify({"data":{"number":order_number, "payment":{"status":res["status"],"message":message}}})
  except:
        res = make_response(jsonify({"error": True,"message": "伺服器內部錯誤"}),500)
        return res

@order_blueprint.route("/order/<orderNumber>",methods=["GET"])
def Get_order(orderNumber):
    token=request.cookies.get('token')
    if token is None:
        res = make_response(jsonify({"error": True,"message": "未登入系統，拒絕存取"}), 403)
        return res
    else:
      db=con_pool.get_connection()
      cursor=db.cursor(dictionary=True,buffered=True)
      sql="""SELECT orders.ordernumber,orders.price,orders.username ,orders.email,orders.phone,orders.date,
      orders.time,orders.attractionId,orders.status,information.name ,information.address,information.images 
      FROM orders INNER JOIN information ON orders.attractionId=information.id WHERE orders.ordernumber=%s """
      val=(orderNumber,)
      cursor.execute(sql, val)
      result=cursor.fetchone()
      db.close()
      if result is not None:
        order_info={
          "number":result["ordernumber"],
          "price":result["price"],
          "trip":{
            "attraction":{
              "id":result["attractionId"],
              "name":result["name"],
              "address":result["address"],
              "image":json.loads(result["images"])[0]
            },
            "date":result["date"],
            "time":result["time"],
          },
          "contact":{
            "name":result["username"],
            "email":result["email"],
            "phone":result["phone"]
          },
          "status":result["status"]
        }
        return jsonify({"data":order_info})
      else:
        res = make_response(jsonify({"data": None,"message": "沒有資料，請確認訂單編號"}), 200)
        return res