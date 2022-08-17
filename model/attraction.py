from model.public import con_pool
import json


def select(index, keyword):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True)
        if keyword is not None:
            cursor.execute("SELECT * FROM attractions WHERE name LIKE %s limit %s OFFSET %s ",
                           (f'%{keyword}%', index+13, index))
            attrs = cursor.fetchall()
            for i in attrs:
                i["images"] = json.loads(i["images"])
            return attrs
        else:
            sql = "SELECT * FROM attractions limit %s OFFSET %s "
            val = (13, index)
            cursor.execute(sql, val)
            attrs = cursor.fetchall()
            for i in attrs:
                i["images"] = json.loads(i["images"])
            return attrs
    finally:
        cursor.close()
        db.close()


def attraction_id(attractionId):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM attractions WHERE id = %s", (attractionId,))
        select_id = cursor.fetchone()
        return select_id
    finally:
        cursor.close()
        db.close()
