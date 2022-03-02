from flask import Blueprint,request,jsonify,make_response
import json
from data.public import con_pool
api_blueprint = Blueprint('api', __name__)
db=con_pool.get_connection()
cursor=db.cursor(dictionary=True)

def select(index,keyword=None):
        if keyword is not None:
            cursor.execute("SELECT * FROM information WHERE name LIKE %s limit %s OFFSET %s ", (f'%{keyword}%',index+12,index))      
            attrs = cursor.fetchall()
            for i in attrs:
                new_images=json.loads(i["images"])
                i["images"]=new_images
            return attrs
        else:
            sql="SELECT * FROM information limit %s OFFSET %s "
            val = (12,index)
            cursor.execute(sql,val)
            attrs = cursor.fetchall()
            for i in attrs:
                new_images=json.loads(i["images"])
                i["images"]=new_images
            return attrs
        
@api_blueprint.route("/attractions",methods=["GET"])
def attractionApi():
    try:
        page =int(request.args.get("page",default=0, type=int))
        keyword = request.args.get('keyword')
        index=page*12
        if keyword is not None:
            attrs=select(index, keyword)
            attrs_next=select(index+12,keyword)
            if not attrs_next:
                nextPage=None
            else:
                nextPage=page+1
           
        else:
            attrs=select(index)
            attra_next=select(index+12)
            if not attra_next:
                nextPage=None
            else:
                nextPage=page+1
        if not attrs:
                response = make_response(jsonify({"error": True,"message": "找不到景點"}),500)
                response.headers['Content-Type'] ='application/json'
                return response
        else:
                response = make_response(jsonify({"nextPage":nextPage,"data":attrs}))
                response.headers['Content-Type'] ='application/json'
                return response
    except: 
        response = make_response(jsonify({"error": True,"message": "伺服器內部錯誤"}),500)
        response.headers['Content-Type'] ='application/json'
        return response

@api_blueprint.route("/attraction/<attractionId>",methods=["GET"])
def attractionId(attractionId):
    try:
        cursor.execute("SELECT * FROM information WHERE id = %s", (attractionId,))
        id = cursor.fetchone()
        new_images=json.loads(id["images"])
        id["images"]=new_images    
        if id is not None:
            response = make_response(jsonify({"data":id}))
            response.headers['Content-Type'] ='application/json'
            return response
        else:
            response = make_response(jsonify({"error": True,"message": "景點編號不正確"}),400)
            response.headers['Content-Type'] ='application/json'
            return response
    except:
        response = make_response(jsonify({"error": True,"message": "伺服器內部錯誤"}),500)
        response.headers['Content-Type'] ='application/json'
        return response


