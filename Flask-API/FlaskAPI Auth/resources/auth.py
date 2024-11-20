#~/FlaskAPI/resources/auth.py

from flask_restful import Resource
from flask import Response, request
from flask_jwt_extended import create_access_token
from database.models import User
from database.db import db, query
import uuid
import datetime

class SignupAPI(Resource):
    def put(self):
        id = uuid.uuid4().hex
        args = User.user_args.parse_args()
        args['id'] = id
        db.insert(args)
        return {'id': str(args['id'])}, 201

class LoginAPI(Resource):
    def put(self):
        args = User.user_args.parse_args()
        savedPasswordQuery = db.search(query.email == args['mail'])
        savedPassword = savedPasswordQuery[0]['password']
        password = args['password']
        authorized = User.check_password(savedPassword, password)
        if not authorized:
            return {'error': 'Mail or password invalid'}, 401
 
        expires = datetime.timedelta(days=7)
        access_token = create_access_token(identity=str(args['id']), expires_delta=expires)
        return {'token': access_token}, 200
