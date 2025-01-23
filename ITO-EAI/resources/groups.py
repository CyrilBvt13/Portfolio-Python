from flask import jsonify
from flask_restful import Resource

from database.models import Group
from database.db import db, groups_table, query

import uuid

class Groups(Resource):

    def get(self):
        """
        Récupère tous les groupes de la table 'group' et les retourne sous forme de liste JSON.
    
        Retourne :
            - Une liste de groupes (dict) en cas de succès.
            - Un code 200 pour indiquer une requête réussie.
        """
        # Récupérer tous les groupes depuis la table "group"
        groups = groups_table.all()
    
        # Vérifier si des groupes existent
        if not groups:
            return {"message": "No groups found"}, 404  # Retourner un message si aucun groupe trouvé

        return {"groups": groups}, 200

    def put(self):
        """
        Crée un nouveau groupe.

        Retourne :
            - L'identifiant du groupe créé (group_id).
        """
        id = uuid.uuid4().hex
        args = Group.group_args.parse_args()
        args['group_id'] = id
        groups_table.insert(args)
        return {"group_id": id}, 200

    def update(self, uid):
        """
        Modifie un groupe existant.

        Paramètres :
            groupe_id (str) : L'identifiant du groupe à modifier.

        Retourne :
            - Le groupe modifié.
            - Un code 404 si le groupe n'existe pas.
        """
        args = Group.group_args.parse_args()
        groups_table.update(args, query.id == uid)
        return db.search(query.id == uid), 200

    def delete(self, uid):
        """
        Supprime un groupe existant.

        Paramètres :
            groupe_id (str) : L'identifiant du groupe à supprimer.

        Retourne :
            - Un code 204 si la suppression réussit.
            - Un code 404 si le groupe n'existe pas.
        """
        groups_table.remove(query.id == uid)
        return '', 204
    