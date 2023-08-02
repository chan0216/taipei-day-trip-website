import json
from common.config.db_config import con_pool

with open("data/taipei-attractions.json",mode="r",encoding="utf-8") as file:
    file = json.load(file)
    all_data = file["result"]["results"]
    for data in all_data:
        imglist=[]
        all_img = data["file"].split("http")[1:]
        for img in all_img:
            filter_img = "http"+img
            if ("jpg" or "png") in filter_img.lower():
                imglist.append(filter_img)
        db = con_pool.get_connection()
        cursor = db.cursor(dictionary=True)
        sql = "INSERT INTO information (name,category,description,address,transport,mrt,latitude,longitude,images) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (data["stitle"],data["CAT2"],data["xbody"],data["address"],data["info"],data["MRT"],data["latitude"],data["longitude"],json.dumps(imglist))
        cursor.execute(sql, val)
        db.commit()
        db.close()

                    




      