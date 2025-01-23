from flask import jsonify
from flask_restful import Resource

from database.models import Flow
from database.db import db, query, flows_table

import uuid

class Flows(Resource):

    def get_by_group(group_id):
        """
        Récupère tous les flux associés à un `group_id`.

        Paramètres :
            group_id (str) : L'identifiant du groupe.

        Retourne :
            - Une liste de flux (dict) en cas de succès.
            - Un message et un code 404 si aucun flux n'est trouvé.
        """
        flows = flows_table.search(query.flow_group_id == group_id)
        if not flows:
            return {"message": f"No flows found for group_id: {group_id}"}, 404
        return {"flows": flows}, 200

    def create():
        """
        Crée un nouveau flux.

        Retourne :
            - L'identifiant du flux créé (flow_id).
        """
        args = Flow.flow_args.parse_args()
        flow_id = uuid.uuid4().hex  # Génère un ID unique pour le flux
        args["flow_id"] = flow_id
        flows_table.insert(args)  # Insère le flux dans la table
        return {"flow_id": flow_id}, 200

    def update(flow_id):
        """
        Modifie un flux existant.

        Paramètres :
            flow_id (str) : L'identifiant du flux à modifier.

        Retourne :
            - Le flux modifié.
            - Un code 404 si le flux n'existe pas.
        """
        args = Flow.flow_args.parse_args()
        updated = flows_table.update(args, query.flow_id == flow_id)
        if not updated:
            return {"message": f"No flow found with id: {flow_id}"}, 404
        return flows_table.search(query.flow_id == flow_id), 200

    def delete(flow_id):
        """
        Supprime un flux existant.

        Paramètres :
            flow_id (str) : L'identifiant du flux à supprimer.

        Retourne :
            - Un code 204 si la suppression réussit.
            - Un code 404 si le flux n'existe pas.
        """
        deleted = flows_table.remove(query.flow_id == flow_id)
        if not deleted:
            return {"message": f"No flow found with id: {flow_id}"}, 404
        return "", 204

"""

Ajout d'un flux : 

    flow_data = {
        "flow_group_id": "group_1",
        "flow_is_active": True,
        "flow_receivers": ["Receiver1", "Receiver2"],
        "flow_transformers": ["Transformer1", "Transformer2"],
        "flow_senders": ["Sender1", "Sender2"],
    }

    with app.test_request_context(json=flow_data):
        response, status_code = Flow.create()
        print("Création d'un flux :", response, status_code)

Recherche d'un flux par group_id :

    group_id = "group_1"

    response, status_code = Flow.get_by_group(group_id)
    if status_code == 200:
        print("Flux associés au groupe :", response)
    else:
        print(response["message"])

Modification d'un flux : 

    flow_id = "id_du_flux_existant"

    flow_update_data = {
        "flow_group_id": "group_2",
        "flow_is_active": False,
        "flow_receivers": ["Receiver3"],
        "flow_transformers": ["Transformer3"],
        "flow_senders": ["Sender3"],
    }

    with app.test_request_context(json=flow_update_data):
        response, status_code = Flow.update(flow_id)
        if status_code == 200:
            print("Flux mis à jour :", response)
        else:
            print(response["message"])

Suppression d'un flux :

    flow_id = "id_du_flux_a_supprimer"

    response, status_code = Flow.delete(flow_id)
    if status_code == 204:
        print("Flux supprimé avec succès.")
    else:
        print(response["message"])

"""