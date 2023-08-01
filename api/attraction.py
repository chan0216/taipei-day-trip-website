import model.attraction
from common.utils.response_util import success,failure
from flask import Blueprint, request

attraction_blueprint = Blueprint('attraction', __name__)

def paginate_attractions(page, keyword=None):
    index = page * 12
    attractions = model.attraction.get_attractions(index, keyword)
    if len(attractions) == 13:
        attractions.pop()
        next_page = page + 1
    else:
        next_page = None
    return next_page, attractions

@attraction_blueprint.route("/attractions", methods=["GET"])
def get_attractions():
    try:
        page = int(request.args.get("page", default=0, type=int))
        keyword = request.args.get('keyword')
        next_page, attractions = paginate_attractions(page, keyword)
        if not attractions:
            return failure("找不到景點", 400)
        else:
            return success(attractions,next_page)
    except:
        return failure()
        

@attraction_blueprint.route("/attraction/<attractionId>", methods=["GET"])
def get_attraction(attractionId):
    try:
        result = model.attraction.get_attraction(attractionId)
        if not result:
            return failure('景點編號不正確',400)
        else:
            return success(result)
    except Exception as e:
        return failure()

