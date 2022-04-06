import jwt
import json
from decouple import config
from flask import Blueprint,request,jsonify,make_response
from model.public import con_pool
booking_blueprint = Blueprint('booking', __name__)

# @booking_blueprint.route("/booking",methods=["POST"])
# def createjourney():
#     try:
#         token=request.cookies.get('token')
#         if token is None:
#                 res = make_response(jsonify({"error": True,"message": "未登入系統，拒絕存取"}), 403)
#                 return res
#         else:
#             data = request.get_json()
#             attractionId=data["attractionId"]
#             date=data["date"]
#             time=data["time"]
#             price=data["price"]
#             if '' not in data.values():
#                 userdata=jwt.decode(token.encode('UTF-8'), config("secret_key"), algorithms=["HS256"])
#                 cursor.execute("SELECT email FROM schedule WHERE email=%s", (userdata["user"],))
#                 userEmail=cursor.fetchone()
#                 if userEmail !=None:
#                     sql="UPDATE schedule SET attractionId=%s,date=%s,time=%s,price=%s WHERE email=%s"
#                     val= (attractionId, date, time, price, userdata["user"] )
#                     cursor.execute(sql, val)
#                     db.commit()
#                     res = make_response(jsonify({"ok": True}), 200)
#                     return res 
#                 else:
#                     cursor.execute("INSERT INTO schedule (attractionId, date, time, price, email) VALUES (%s, %s, %s, %s, %s)",
#                     (attractionId, date, time, price, userdata["user"] ))
#                     db.commit()
#                     res = make_response(jsonify({"ok": True}), 200)
#                     return res
#             else:
#                 res = make_response(jsonify({"error": True,"message": "建立失敗，輸入不正確"}), 400)
#                 return res
         
#     except:
#         response = make_response(jsonify({"error": True,"message": "伺服器內部錯誤"}),500)
#         return response

# @booking_blueprint.route("/booking",methods=["GET"])
# def getjourney():
#     token=request.cookies.get('token')
#     if token is None:
#         res = make_response(jsonify({"error": True,"message": "未登入系統，拒絕存取"}), 403)
#         return res
#     else:
#         userdata=jwt.decode(token.encode('UTF-8'), config("secret_key"), algorithms=["HS256"])
#         cursor.execute("SELECT information.id,information.name,information.address,information.images,schedule.date,schedule.time,schedule.price FROM information INNER JOIN schedule ON information.id=schedule.attractionId WHERE schedule.email=%s",(userdata["user"],))
#         result=cursor.fetchone()
#         print(result)
#         if result is None:
#             return jsonify({"data": None})
#         else:
#             result["images"]=json.loads(result["images"])
#             booking_info={"attraction":{
#                 "id":result["id"],
#                 "name":result["name"],
#                 "address":result["address"],
#                 "image":result["images"][0]},
#                 "date":result["date"],
#                 "time":result["time"],
#                 "price":result["price"]
#                 }
#             return jsonify({"data":booking_info})


# @booking_blueprint.route("/booking",methods=["DELETE"])
# def handle_delete():
#     token=request.cookies.get('token')
#     if token is None:
#         res = make_response(jsonify({"error": True,"message": "未登入系統，拒絕存取"}), 403)
#         return res
#     else:
#         userdata=jwt.decode(token.encode('UTF-8'), config("secret_key"), algorithms=["HS256"])
#         cursor.execute("DELETE FROM schedule WHERE email=%s",(userdata['user'],))
#         db.commit()
#         res = make_response(jsonify({"ok": True}), 200)
#         return res 
@booking_blueprint.route("/booking",methods=["DELETE"])
def handle_delete():
    result=AttractionModel.delete()
    return AttractionView.renderdelete(result)

@booking_blueprint.route("/booking",methods=["POST"])
def handle_post():
    data = request.get_json()
    result=AttractionModel.get_post(data)
    return AttractionView.renderpost(result)

@booking_blueprint.route("/booking",methods=["GET"])
def handle_get():
    result=AttractionModel.get()
    return AttractionView.renderget(result)

class AttractionView:
    def renderpost(self,result):
        token=request.cookies.get('token')
        if token is None:
            res = make_response(jsonify({"error": True,"message": "未登入系統，拒絕存取"}), 403)
            return res
        else:
            if result=="ok":
                res = make_response(jsonify({"ok": True}), 200)
                return res
            elif result=="error":
                res = make_response(jsonify({"error": True,"message": "伺服器內部錯誤"}),500)
                return res
            else:
                res = make_response(jsonify({"error": True,"message": "建立失敗，輸入不正確"}), 400)
                return res
    def renderget(self,result):
        token=request.cookies.get('token')
        if token is None:
            res = make_response(jsonify({"error": True,"message": "未登入系統，拒絕存取"}), 403)
            return res
        else:
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
    def renderdelete(self,result):
        token=request.cookies.get('token')
        if token is None:
            res = make_response(jsonify({"error": True,"message": "未登入系統，拒絕存取"}), 403)
            return res
        else:
            if result=="ok":
                res = make_response(jsonify({"ok": True}), 200)
                return res
AttractionView=AttractionView()

            

class AttractionModel:
    def get_post(self,data):
        try:
            token=request.cookies.get('token')
            db=con_pool.get_connection()
            cursor=db.cursor(dictionary=True,buffered=True)
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
                    return "ok"
                else:
                    cursor.execute("INSERT INTO schedule (attractionId, date, time, price, email) VALUES (%s, %s, %s, %s, %s)",
                    (attractionId, date, time, price, userdata["user"] ))
                    db.commit()
                    return "ok"
            return "資料不完整"
        except:
            return "error"
        finally:
            db.close()

    def get(self):
        try:
            db=con_pool.get_connection()
            cursor=db.cursor(dictionary=True,buffered=True)
            token=request.cookies.get('token')
            userdata=jwt.decode(token.encode('UTF-8'), config("secret_key"), algorithms=["HS256"])
            cursor.execute("SELECT information.id,information.name,information.address,information.images,schedule.date,schedule.time,schedule.price FROM information INNER JOIN schedule ON information.id=schedule.attractionId WHERE schedule.email=%s",(userdata["user"],))
            result=cursor.fetchone()
            return result
        except:
            return "error"
        finally:
            db.close()

    def delete(self):
        try:
            token=request.cookies.get('token')
            db=con_pool.get_connection()
            cursor=db.cursor(dictionary=True,buffered=True)
            userdata=jwt.decode(token.encode('UTF-8'), config("secret_key"), algorithms=["HS256"])
            cursor.execute("DELETE FROM schedule WHERE email=%s",(userdata['user'],))
            db.commit()
            return "ok"
        except:
            print("db error")
        finally:
            db.close()
AttractionModel=AttractionModel()