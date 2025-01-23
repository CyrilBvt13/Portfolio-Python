def create_sender(sender_data):
    """
    Crée un FlowSender à partir des données fournies.
    """
    return {
        "sender_id": sender_data.get("sender_id"),
        "sender_name": sender_data["sender_name"],
        "sender_is_tcp": sender_data["sender_is_tcp"],
        "sender_is_sftp": sender_data["sender_is_sftp"],
        "sender_host": sender_data.get("sender_host"),
        "sender_port": sender_data.get("sender_port"),
        "sender_login": sender_data.get("sender_login"),
        "sender_pwd": sender_data.get("sender_pwd"),
    }