from common.config.db_config import con_pool


def post_booking(data, current_user):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True, buffered=True)
        attraction_id = data["attractionId"]
        date = data["date"]
        time = data["time"]
        price = data["price"]
        if '' not in data.values():
            cursor.execute(
                "SELECT user_id FROM booking WHERE user_id=%s", (current_user,))
            user_id = cursor.fetchone()
            if user_id != None:
                sql = "UPDATE booking SET attraction_id=%s,date=%s,time=%s,price=%s WHERE user_id=%s"
                val = (attraction_id, date, time, price, current_user)
                cursor.execute(sql, val)
                db.commit()
                return "ok"
            else:
                cursor.execute("INSERT INTO booking (attraction_id, date, time, price, user_id) VALUES (%s, %s, %s, %s, %s)",
                               (attraction_id, date, time, price, current_user))
                db.commit()
                return "ok"
        return "資料不完整"
    except:
        return "error"
    finally:

        db.close()


def get_booking(current_user):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True, buffered=True)
        cursor.execute("SELECT attractions.id,attractions.name,attractions.address,attractions.images,booking.date,booking.time,booking.price FROM attractions INNER JOIN booking ON attractions.id=booking.attraction_id WHERE booking.user_id=%s", (current_user,))
        result = cursor.fetchone()
        return result
    except:
        return "error"
    finally:
        cursor.close()
        db.close()


def delete_booking(current_user):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True, buffered=True)
        cursor.execute(
            "DELETE FROM booking WHERE user_id=%s", (current_user,))
        return "ok"
    except:
        db.rollback()
    finally:
        cursor.close()
        db.commit()
        db.close()
