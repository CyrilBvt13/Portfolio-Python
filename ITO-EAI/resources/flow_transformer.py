def create_transformer(transformer_data):
    """
    Crée un FlowTransformer à partir des données fournies.
    """
    return {
        "transformer_id": transformer_data.get("transformer_id"),
        "transformer_name": transformer_data["transformer_name"],
        "transformer_receivers": transformer_data["transformer_receivers"],
        "transformer_senders": transformer_data["transformer_senders"],
        "transformer_rules": transformer_data["transformer_rules"],
    }