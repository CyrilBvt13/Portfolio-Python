from flask_restful import reqparse
from flask_bcrypt import generate_password_hash, check_password_hash

class Group:
    group_args = reqparse.RequestParser()
    group_args.add_argument("group_id", type=str)
    group_args.add_argument("group_name", type=str, help="group name is missing", required=True)

class User:
    user_args = reqparse.RequestParser()
    user_args.add_argument("id", type=str)
    user_args.add_argument("username", type=str, help="username is missing", required=True)
    user_args.add_argument("password", type=str, help="password is missing", required=True)
    
    def hash_password(password):
        hashedPassword = generate_password_hash(password).decode('utf8')
        return hashedPassword
 
    def check_password(hashedPassword, password):
        return check_password_hash(hashedPassword, password)