def success(data=None):
    if data is None:
        return {'ok': True}, 200
    return {
        'ok': True,
        'data': data
    }, 200

def failure(message="伺服器內部錯誤，請稍後再試", status_code=500):
    return {
        "error": True,
        "message": message
    }, status_code
