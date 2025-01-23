def create_receiver(receiver_data):
    """
    Crée un FlowReceiver à partir des données fournies.
    """
    return {
        "receiver_id": receiver_data.get("receiver_id"),
        "receiver_name": receiver_data["receiver_name"],
        "receiver_is_tcp": receiver_data["receiver_is_tcp"],
        "receiver_is_sftp": receiver_data["receiver_is_sftp"],
        "receiver_host": receiver_data.get("receiver_host"),
        "receiver_port": receiver_data.get("receiver_port"),
        "receiver_login": receiver_data.get("receiver_login"),
        "receiver_pwd": receiver_data.get("receiver_pwd"),
    }