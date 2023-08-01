from flask import Blueprint, request, jsonify, make_response
import json
import model.attraction
api_blueprint = Blueprint('api', __name__)


def select(index, keyword=None):
    result = model.attraction.select(index, keyword)
    return result


@api_blueprint.route("/attractions", methods=["GET"])
def attraction_api():
    try:
        page = int(request.args.get("page", default=0, type=int))
        keyword = request.args.get('keyword')
        index = page*12
        if keyword is not None:
            attrs = select(index, keyword)
            if len(attrs) == 13:
                nextPage = page+1
                attrs.pop(12)
            else:
                nextPage = None

        else:
            attrs = select(index)
            if len(attrs) == 13:
                nextPage = page+1
                attrs.pop(12)
            else:
                nextPage = None

        if not attrs:
            response = make_response(
                jsonify({"error": True, "message": "找不到景點"}), 400)
            response.headers['Content-Type'] = 'application/json'
            return response
        else:
            response = make_response(
                jsonify({"nextPage": nextPage, "data": attrs}))
            response.headers['Content-Type'] = 'application/json'
            return response
    except:
        response = make_response(
            jsonify({"error": True, "message": "伺服器內部錯誤"}), 500)
        response.headers['Content-Type'] = 'application/json'
        return response


@api_blueprint.route("/attraction/<attractionId>", methods=["GET"])
def attraction_id(attractionId):
    try:
        result = model.attraction.attraction_id(attractionId)

        if result is None:
            response = make_response(
                {"error": True, "message": "景點編號不正確"}, 400)
            response.headers['Content-Type'] = 'application/json'
            return response
        else:
            result["images"] = json.loads(result["images"])
            response = make_response(jsonify({"data": result}))
            response.headers['Content-Type'] = 'application/json'
            return response
    except:
        response = make_response(
            jsonify({"error": True, "message": "伺服器內部錯誤"}), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

