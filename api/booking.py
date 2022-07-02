import jwt
import json
from functools import wraps
from decouple import config
from flask import Blueprint, request, jsonify, make_response
from model.public import con_pool
booking_blueprint = Blueprint('booking', __name__)


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
            current_user = jwtdata["user"]
        except Exception as e:
            res = make_response(
                jsonify({"error": True, "message": "伺服器內部錯誤"}), 500)
            return res
        return f(current_user)
    return decorated


@booking_blueprint.route("/booking", methods=["DELETE"])
@token_required
def handle_delete(current_user):
    result = AttractionModel.delete(current_user)
    return AttractionView.renderdelete(result)


@booking_blueprint.route("/booking", methods=["POST"])
@token_required
def handle_post(current_user):
    data = request.get_json()
    result = AttractionModel.get_post(data, current_user)
    return AttractionView.renderpost(result)


@booking_blueprint.route("/booking", methods=["GET"])
@token_required
def handle_get(current_user):
    result = AttractionModel.get(current_user)
    return AttractionView.renderget(result)


class AttractionView:
    def renderpost(self, result):
        if result == "ok":
            res = make_response(jsonify({"ok": True}), 200)
            return res
        elif result == "error":
            res = make_response(
                jsonify({"error": True, "message": "伺服器內部錯誤"}), 500)
            return res
        else:
            res = make_response(
                jsonify({"error": True, "message": "建立失敗，輸入不正確"}), 400)
            return res

    def renderget(self, result):
        if result is None:
            return jsonify({"data": None})
        else:
            result["images"] = json.loads(result["images"])
            booking_info = {"attraction": {
                "id": result["id"],
                "name": result["name"],
                "address": result["address"],
                "image": result["images"][0]},
                "date": result["date"],
                "time": result["time"],
                "price": result["price"]
            }
            return jsonify({"data": booking_info})

    def renderdelete(self, result):
        if result == "ok":
            res = make_response(jsonify({"ok": True}), 200)
            return res


AttractionView = AttractionView()


class AttractionModel:
    def get_post(self, data, current_user):
        try:
            db = con_pool.get_connection()
            cursor = db.cursor(dictionary=True, buffered=True)
            attractionId = data["attractionId"]
            date = data["date"]
            time = data["time"]
            price = data["price"]
            if '' not in data.values():
                cursor.execute(
                    "SELECT email FROM schedule WHERE email=%s", (current_user,))
                userEmail = cursor.fetchone()
                if userEmail != None:
                    sql = "UPDATE schedule SET attractionId=%s,date=%s,time=%s,price=%s WHERE email=%s"
                    val = (attractionId, date, time, price, current_user)
                    cursor.execute(sql, val)
                    return "ok"
                else:
                    cursor.execute("INSERT INTO schedule (attractionId, date, time, price, email) VALUES (%s, %s, %s, %s, %s)",
                                   (attractionId, date, time, price, current_user))
                    return "ok"
            return "資料不完整"
        except:
            return "error"
        finally:
            db.commit()
            db.close()

    def get(self, current_user):
        try:
            db = con_pool.get_connection()
            cursor = db.cursor(dictionary=True, buffered=True)
            cursor.execute("SELECT information.id,information.name,information.address,information.images,schedule.date,schedule.time,schedule.price FROM information INNER JOIN schedule ON information.id=schedule.attractionId WHERE schedule.email=%s", (current_user,))
            result = cursor.fetchone()
            return result
        except:
            return "error"
        finally:
            cursor.close()
            db.close()

    def delete(self, current_user):
        try:
            db = con_pool.get_connection()
            cursor = db.cursor(dictionary=True, buffered=True)
            cursor.execute(
                "DELETE FROM schedule WHERE email=%s", (current_user,))
            return "ok"
        except:
            db.rollback()
        finally:
            cursor.close()
            db.commit()
            db.close()


AttractionModel = AttractionModel()
