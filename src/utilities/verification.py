import jwt, os
from flask import request, jsonify
from src.models.user import User
from functools import wraps

SECRET_KEY = os.getenv("SECRET_KEY")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            if ("user_id" not in data) or ("email" not in data):
                return jsonify({'message': 'Invalid token!'}), 401
        except jwt.ExpiredSignatureError:
            print("test-here")
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            print('hdbadba')
            return jsonify({'message': 'Invalid token!'}), 401

        return f(*args, **kwargs)
    
    return decorated


def get_token_data(token):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        if "user_id" not in data or "email" not in data:
            return False, "Data is invalid"
        else:
            return True, {
                "user_id": str(data['user_id']),
                "email_id": str(data['email'])
            }
    except Exception as err:
        return False, str(err)


def get_token_user():
    try:
        auth_header = request.headers['Authorization']
        token = auth_header.split(" ")[1]
        status, data = get_token_data(token)
        return data
    except Exception as err:
        return {}
