from common.config.db_config import con_pool


def get_order(orderNumber):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True, buffered=True)
        sql = """SELECT orders.ordernumber,orders.price,orders.username ,orders.email,orders.phone,orders.date,
        orders.time,orders.attraction_id,orders.status,attractions.name ,attractions.address,attractions.images 
        FROM orders INNER JOIN attractions ON orders.attraction_id=attractions.id WHERE orders.ordernumber=%s"""
        val = (orderNumber,)
        cursor.execute(sql, val)
        result = cursor.fetchone()
        return result
    except:
        return "error"
    finally:
        cursor.close()
        db.close()


def post_order(order_number, data, current_user, name, email, phone_number, res, message):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True)
        sql = "Insert Into orders(ordernumber, price, user_id,username, email, phone, date, time, attraction_id,status) Values(%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"
        val = (order_number, data["order"]["price"], current_user, name, email, phone_number, data["order"]["trip"]
               ["date"], data["order"]["trip"]["time"], data["order"]["trip"]["attraction"]["id"], res["status"])
        cursor.execute(sql, val)
        db.commit()
        cursor.execute("DELETE FROM booking WHERE user_id=%s", (current_user,))
        db.commit()
        return {"data": {"number": order_number, "payment": {"status": res["status"], "message": message}}}
    except:
        db.rollback()
        return "error"
    finally:
        cursor.close()
        db.close()
