import hl7
from core.rule_engine import RuleEngine

def process_hl7_file(content, rules_path=None):
    try:
        h = hl7.parse(content)
        if rules_path:
            rule_engine = RuleEngine()
            rule_engine.load_rules(rules_path)
            h = rule_engine.apply_rules(h)
        return str(h)
    except Exception as e:
        print(f"Erreur de traitement HL7 : {e}")
        return None


from hl7apy.parser import parse_message
from rules_engine import apply_rules

def process_hl7_message(raw_message, rules):
    # Parser le message HL7
    hl7_message = parse_message(raw_message)

    # Appliquer les règles au message
    modified_message = apply_rules(hl7_message, rules)

    # Retourner le message modifié en format HL7
    return hl7_message.to_er7()