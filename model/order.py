from common.config.db_config import con_pool


def get_order(order_number):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True, buffered=True)
        sql = """SELECT orders.order_number,orders.price,orders.name,orders.email,orders.phone,DATE_FORMAT(orders.date, '%Y-%m-%d') as date,
        orders.time_period,orders.attraction_id,orders.status,attractions.name,attractions.address,attractions.images 
        FROM orders INNER JOIN attractions ON orders.attraction_id=attractions.id WHERE orders.order_number=%s"""
        val = (order_number,)
        cursor.execute(sql, val)
        result = cursor.fetchone()
        return result
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()


def post_order(current_user,order_number, data, status):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True)
        sql = "Insert Into orders(order_number, price, user_id, name, email, phone, date, time_period, attraction_id, status) Values(%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"
        val = (order_number, data["order"]["price"], current_user, data["order"]["contact"]["name"], data["order"]["contact"]["email"], data["order"]["contact"]["phone"], 
               data["order"]["trip"]["date"], data["order"]["trip"]["time"], data["order"]["trip"]["attraction"]["id"], status)
        cursor.execute(sql, val)
        cursor.execute("DELETE FROM booking WHERE user_id=%s", (current_user,))
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()
        db.close()
