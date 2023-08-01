def success(data=None, next_page=None):
    response = {'ok': True}
    if data:
        response['data'] = data
    if next_page is not None:
        response['nextPage'] = next_page
    return response, 200

def failure(message="伺服器內部錯誤，請稍後再試", status_code=500):
    return {
        "error": True,
        "message": message
    }, status_code
