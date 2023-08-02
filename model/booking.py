import json
from common.config.db_config import con_pool


def post_booking(data, current_user):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True, buffered=True)
        attraction_id = data["attractionId"]
        date = data["date"]
        time = data["time"]
        price = data["price"]
        if not all([attraction_id, date, time, price]):
            raise ValueError('欄位不得為空')
        cursor.execute(
            "SELECT user_id FROM booking WHERE user_id=%s", (current_user,))
        user_id = cursor.fetchone()
        if user_id:
            sql = "UPDATE booking SET attraction_id=%s,date=%s,time_period=%s,price=%s WHERE user_id=%s"
            val = (attraction_id, date, time, price, current_user)
            cursor.execute(sql, val)
        else:
            cursor.execute("INSERT INTO booking (attraction_id, date, time_period, price, user_id) VALUES (%s, %s, %s, %s, %s)",
                            (attraction_id, date, time, price, current_user))
        db.commit()
        return True
    except Exception as e:
        raise(e)
    finally:
        cursor.close()
        db.close()



def get_booking(current_user):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True, buffered=True)
        cursor.execute("""SELECT attractions.id,attractions.name,attractions.address,attractions.images,DATE_FORMAT(booking.date, '%Y-%m-%d') as date,booking.time_period,booking.price 
                       FROM attractions INNER JOIN booking ON attractions.id=booking.attraction_id WHERE booking.user_id=%s""", (current_user,))
        result = cursor.fetchone()
        if result:
            result["images"] = json.loads(result["images"])
        return result
    except Exception as e:
        raise e
    finally:
        cursor.close()
        db.close()


def delete_booking(current_user):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True, buffered=True)
        cursor.execute(
            "DELETE FROM booking WHERE user_id=%s", (current_user,))
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()
        db.close()
