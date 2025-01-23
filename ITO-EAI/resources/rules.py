def create_rule(rule_data):
    """
    Crée une règle pour un transformer.
    """
    return {
        "rule_id": rule_data.get("rule_id"),
        "rule_name": rule_data.get("rule_name"),
        "rule_conditions": rule_data.get("rule_conditions"),
        "rule_actions": rule_data.get("rule_actions"),
    }