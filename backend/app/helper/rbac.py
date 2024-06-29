from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

USER_LEVELS = {
    "super_admin": 0,
    "operator": 1,
    "professor": 2,
    "student": 3
}

def user_level_required(minimum_level):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("user_level") is not None and claims["user_level"] <= minimum_level:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Access forbidden: insufficient user level"), 403
        return decorator
    return wrapper
