
from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def jwt_required():
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                return fn(*args, **kwargs)
            except Exception as e:
                return jsonify({'error': 'Invalid or missing token'}), 401
        return wrapper
    return decorator

def role_required(role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                claims = get_jwt()
                if claims.get('role') != role:
                    return jsonify({'error': 'Insufficient permissions'}), 403
                return fn(*args, **kwargs)
            except Exception as e:
                return jsonify({'error': 'Invalid or missing token'}), 401
        return wrapper
    return decorator