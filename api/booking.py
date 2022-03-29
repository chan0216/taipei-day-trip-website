import jwt
import json
from decouple import config
from flask import Blueprint,request,jsonify,make_response
from model.public import con_pool
booking_blueprint = Blueprint('booking', __name__)
db=con_pool.get_connection()
cursor=db.cursor(dictionary=True,buffered=True)
@booking_blueprint.route("/booking",methods=["POST"])
def createjourney():
    try:
        token=request.cookies.get('token')
        if token is None:
                res = make_response(jsonify({"error": True,"message": "未登入系統，拒絕存取"}), 403)
                return res
        else:
            data = request.get_json()
            attractionId=data["attractionId"]
            date=data["date"]
            time=data["time"]
            price=data["price"]
            if '' not in data.values():
                userdata=jwt.decode(token.encode('UTF-8'), config("secret_key"), algorithms=["HS256"])
                cursor.execute("SELECT email FROM schedule WHERE email=%s", (userdata["user"],))
                userEmail=cursor.fetchone()
                if userEmail !=None:
                    sql="UPDATE schedule SET attractionId=%s,date=%s,time=%s,price=%s WHERE email=%s"
                    val= (attractionId, date, time, price, userdata["user"] )
                    cursor.execute(sql, val)
                    db.commit()
                    res = make_response(jsonify({"ok": True}), 200)
                    return res 
                else:
                    cursor.execute("INSERT INTO schedule (attractionId, date, time, price, email) VALUES (%s, %s, %s, %s, %s)",
                    (attractionId, date, time, price, userdata["user"] ))
                    db.commit()
                    res = make_response(jsonify({"ok": True}), 200)
                    return res
            else:
                res = make_response(jsonify({"error": True,"message": "建立失敗，輸入不正確"}), 400)
                return res
         
    except:
        response = make_response(jsonify({"error": True,"message": "伺服器內部錯誤"}),500)
        return response

@booking_blueprint.route("/booking",methods=["GET"])
def getjourney():
    token=request.cookies.get('token')
    if token is None:
        res = make_response(jsonify({"error": True,"message": "未登入系統，拒絕存取"}), 403)
        return res
    else:
        userdata=jwt.decode(token.encode('UTF-8'), config("secret_key"), algorithms=["HS256"])
        cursor.execute("SELECT information.id,information.name,information.address,information.images,schedule.date,schedule.time,schedule.price FROM information INNER JOIN schedule ON information.id=schedule.attractionId WHERE schedule.email=%s",(userdata["user"],))
        result=cursor.fetchone()
        if result is None:
            return jsonify({"data": None})
        else:
            result["images"]=json.loads(result["images"])
            booking_info={"attraction":{
                "id":result["id"],
                "name":result["name"],
                "address":result["address"],
                "image":result["images"][0]},
                "date":result["date"],
                "time":result["time"],
                "price":result["price"]
                }
            return jsonify({"data":booking_info})


@booking_blueprint.route("/booking",methods=["DELETE"])
def deletejourney():
    token=request.cookies.get('token')
    if token is None:
        res = make_response(jsonify({"error": True,"message": "未登入系統，拒絕存取"}), 403)
        return res
    else:
        userdata=jwt.decode(token.encode('UTF-8'), config("secret_key"), algorithms=["HS256"])
        cursor.execute("DELETE FROM schedule WHERE email=%s",(userdata['user'],))
        db.commit()
        res = make_response(jsonify({"ok": True}), 200)
        return res 

