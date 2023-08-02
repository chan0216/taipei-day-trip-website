import json
from common.config.db_config import con_pool



def get_attractions(index, keyword):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True)
        if keyword is not None:
            sql = "SELECT * FROM attractions WHERE name LIKE %s limit %s OFFSET %s "
            val = (f'%{keyword}%', index+13, index)
        else:
            sql = "SELECT * FROM attractions limit %s OFFSET %s "
            val = (13, index)
        cursor.execute(sql, val)
        attractions = cursor.fetchall()
        for obj in attractions:
            obj["images"] = json.loads(obj["images"])
        return attractions
    finally:
        cursor.close()
        db.close()



def get_attraction(attractionId):
    try:
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM attractions WHERE id = %s", (attractionId,))
        attraction = cursor.fetchone()
        if attraction:
            attraction["images"] = json.loads(attraction["images"])
        return attraction
    finally:
        cursor.close()
        db.close()
