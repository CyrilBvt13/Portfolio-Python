import flet as ft

def show_error(page, message):
    """
    Affiche une boîte de dialogue d'erreur contenant le message spécifié.
    La boîte de dialogue offre un bouton "OK" pour la fermer.

    Paramètres :
        page (ft.Page) : L'objet représentant la page de l'application.
        message (str) : Le message d'erreur à afficher dans la boîte de dialogue.
    """
    
    def handle_close(e):
        """
        Fonction pour fermer la boîte de dialogue lorsqu'on clique sur "OK".
        
        Paramètres :
            e (ft.Event) : L'événement déclenché lors du clic sur le bouton "OK".
        """
        error_dialog.open = False  # Fermer la boîte de dialogue
        page.update()  # Mettre à jour la page pour refléter les changements
        
    # Création de l'AlertDialog pour afficher le message d'erreur
    error_dialog = ft.AlertDialog(
        content=ft.Text("Une erreur est survenue."),  # Texte par défaut dans la boîte de dialogue
        actions=[  # Liste des actions dans la boîte de dialogue
            ft.TextButton("OK", on_click=handle_close)  # Bouton "OK" pour fermer la boîte de dialogue
        ],
        actions_alignment=ft.MainAxisAlignment.END,  # Alignement des actions (boutons)
        open=False,  # La boîte de dialogue est initialement fermée
    )
    
    # Mise à jour du contenu de la boîte de dialogue avec le message d'erreur passé en paramètre
    error_dialog.content.value = message
    error_dialog.open = True  # Ouvrir la boîte de dialogue
    page.dialog = error_dialog  # Associer la boîte de dialogue à la page
    page.update()  # Mettre à jour la page pour afficher la boîte de dialogue