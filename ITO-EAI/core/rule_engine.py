import json

class RuleEngine:
    def __init__(self):
        self.rules = []

    def add_rule(self, field, action, value=None):
        """
        Ajoute une règle.
        :param field: Champ à modifier.
        :param action: Action ('modify', 'delete', 'add').
        :param value: Nouvelle valeur (si applicable).
        """
        self.rules.append({"field": field, "action": action, "value": value})

    def apply_rules(hl7_message, rules):
        """
        Applique les règles à un message.
        :param message: Message (HL7, XML, ou CSV).
        :return: Message modifié.
        """
        for rule in rules:
            if rule["action"] == "copy":
                source = rule["source"]
                target = rule["target"]
                # Copier la valeur source vers target
                setattr(hl7_message, target, getattr(hl7_message, source))
            elif rule["action"] == "set":
                field = rule["field"]
                value = rule["value"]
                # Définir une valeur spécifique
                setattr(hl7_message, field, value)
        return hl7_message

    def save_rules(self, file_path):
        """Sauvegarde les règles dans un fichier JSON."""
        with open(file_path, 'w') as f:
            json.dump(self.rules, f)

    def load_rules(self, file_path):
        """Charge les règles à partir d'un fichier JSON."""
        with open(file_path, 'r') as f:
            self.rules = json.load(f)

