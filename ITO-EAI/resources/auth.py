import jwt
from flask import request, jsonify

SECRET_KEY = 'ma clé secrète'

def generate_token(user_id):
    payload = {"user_id": user_id}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None