from flask_restful import reqparse
from flask_bcrypt import generate_password_hash, check_password_hash

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

class Group:
    group_args = reqparse.RequestParser()
    group_args.add_argument("group_id", type=str)
    group_args.add_argument("group_name", type=str, help="group name is missing", required=True)

class Flow:
    flow_args = reqparse.RequestParser()
    flow_args.add_argument("flow_id", type=str)
    flow_args.add_argument("flow_group_id", type=str, help="group id is missing", required=True)
    flow_args.add_argument("flow_name", type=str, help="flow name is missing", required=True)
    flow_args.add_argument("flow_is_active", type=bool)
    flow_args.add_argument("flow_receivers", type=list, location='json', help="flow receivers are missing")
    flow_args.add_argument("flow_transformers", type=list, location='json', help="flow transformers are missing")
    flow_args.add_argument("flow_senders", type=list, location='json', help="flow senders are missing")

class FlowReceiver:
    receiver_args = reqparse.RequestParser()
    receiver_args.add_argument("receiver_id", type=str)
    receiver_args.add_argument("receiver_name", type=str, help="receiver name is missing", required=True)
    receiver_args.add_argument("receiver_is_tcp", type=bool, help="is_tcp is missing", required=True)
    receiver_args.add_argument("receiver_is_sftp", type=bool, help="is_sftp is missing", required=True)
    receiver_args.add_argument("receiver_host", type=str)
    receiver_args.add_argument("receiver_port", type=float)
    receiver_args.add_argument("receiver_login", type=str)
    receiver_args.add_argument("receiver_pwd", type=str)
    #receiver_args.add_argument("receiver_key", type=str)

class FlowSender:
    sender_args = reqparse.RequestParser()
    sender_args.add_argument("sender_id", type=str)
    sender_args.add_argument("sender_name", type=str, help="sender name is missing", required=True)
    sender_args.add_argument("sender_is_tcp", type=bool, help="is_tcp is missing", required=True)
    sender_args.add_argument("sender_is_sftp", type=bool, help="is_sftp is missing", required=True)
    sender_args.add_argument("sender_host", type=str)
    sender_args.add_argument("sender_port", type=float)
    sender_args.add_argument("sender_login", type=str)
    sender_args.add_argument("sender_pwd", type=str)
    #sender_args.add_argument("receiver_key", type=str)
    
class FlowTransformer:
    transformer_args = reqparse.RequestParser()
    transformer_args.add_argument("transformer_id", type=str)
    transformer_args.add_argument("transformer_name", type=str, help="transformer name is missing", required=True)
    transformer_args.add_argument("transformer_receivers", type=list, help="transformer_receivers are missing", required=True)
    transformer_args.add_argument("transformer_senders", type=list, help="transformer_senders are missing", required=True)
    transformer_args.add_argument("transformer_rules", type=list, help="rules are missing", required=True)

class Rule:
    rule_args = reqparse.RequestParser()
    rule_args.add_argument("rule_id", type=str)
    rule_args.add_argument("rule_conditions", type=list, required=True)
    rule_args.add_argument("rule_actions", type=list, required=True)

    '''
    Actions possibles :
        - Set
        - Delete
        - Copy
        - Troncate
        - Condition
    '''

class Alert:
    rule_args = reqparse.RequestParser()
    rule_args.add_argument("alert_id", type=str)
    rule_args.add_argument("alert_flow_id", type=str, required=True)
    rule_args.add_argument("alert_date", type=str, required=True)
    rule_args.add_argument("alert_message", type=str, required=True)