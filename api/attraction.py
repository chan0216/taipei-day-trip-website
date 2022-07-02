from flask import Blueprint,request,jsonify,make_response
import json
from model.public import con_pool
api_blueprint = Blueprint('api', __name__)

def select(index,keyword=None):
    try:
        db=con_pool.get_connection()
        cursor=db.cursor(dictionary=True)
        if keyword is not None:
            cursor.execute("SELECT * FROM information WHERE name LIKE %s limit %s OFFSET %s ", (f'%{keyword}%',index+13,index))      
            attrs = cursor.fetchall()
            for i in attrs:
                i["images"]=json.loads(i["images"])
            return attrs
        else:
            sql="SELECT * FROM information limit %s OFFSET %s "
            val = (13,index)
            cursor.execute(sql,val)
            attrs = cursor.fetchall()
            for i in attrs:
                i["images"]=json.loads(i["images"])
            return attrs
    finally:
        cursor.close()
        db.close()
        
@api_blueprint.route("/attractions",methods=["GET"])
def attractionApi():
    try:
        page =int(request.args.get("page",default=0, type=int))
        keyword = request.args.get('keyword')
        index=page*12
        if keyword is not None:
            attrs=select(index, keyword)
            if len(attrs)==13:
                nextPage=page+1
                attrs.pop(12)
            else:
                nextPage=None
            
        else:
            attrs=select(index)
            if len(attrs)==13:
                nextPage=page+1
                attrs.pop(12)
            else:
                nextPage=None
            
        if not attrs:
                response = make_response(jsonify({"error": True,"message": "找不到景點"}),400)
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
        db=con_pool.get_connection()
        cursor=db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM information WHERE id = %s", (attractionId,))
        selectid = cursor.fetchone()
        if selectid  is None:
            response = make_response({"error": True,"message": "景點編號不正確"},400)
            response.headers['Content-Type'] ='application/json'
            return response
        else:
            selectid["images"]=json.loads(selectid["images"])
            response = make_response(jsonify({"data":selectid}))
            response.headers['Content-Type'] ='application/json'
            return response
    except:
        response = make_response(jsonify({"error": True,"message": "伺服器內部錯誤"}),500)
        response.headers['Content-Type'] ='application/json'
        return response
    finally:
        cursor.close()
        db.close()

