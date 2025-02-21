import flet as ft
from core.rule_engine import RuleEngine

rule_engine = RuleEngine()

def create_interface():
    def button_click(e):
        print("Bouton cliqué!")

    page = ft.Page()
    page.title = "Interface EAI"
    page.add(ft.Text("Bienvenue sur l'EAI"))
    page.add(ft.ElevatedButton("Cliquez ici", on_click=button_click))
    return page

def create_rule_interface():
    def add_rule(e):
        field = field_input.value
        action = action_dropdown.value
        value = value_input.value

        if action == "delete":
            value = None

        rule_engine.add_rule(field, action, value)
        rules_list.controls.append(ft.Text(f"{action} '{field}' -> '{value}'"))
        page.update()

    page = ft.Page()
    page.title = "Modification des messages"

    field_input = ft.TextField(label="Champ", width=300)
    action_dropdown = ft.Dropdown(
        label="Action", 
        options=[ft.dropdown.Option("modify"), ft.dropdown.Option("delete"), ft.dropdown.Option("add")]
    )
    value_input = ft.TextField(label="Valeur (si applicable)", width=300)

    add_button = ft.ElevatedButton("Ajouter règle", on_click=add_rule)
    rules_list = ft.Column()

    page.add(ft.Row([field_input, action_dropdown, value_input, add_button]))
    page.add(ft.Text("Règles créées :"))
    page.add(rules_list)

    return page