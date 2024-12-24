import flet as ft
from dicom_handler import process_dicom_file, save_dicom_file
from views.view_menu import create_menu
from views.view_filename import create_file_name
from views.view_file_explorer import create_file_explorer
from views.view_sending import create_tcp_form

def AppView(page):
    """
    Crée l'interface utilisateur principale de l'application.

    Paramètres :
        page (ft.Page) : Page principale de l'application.

    Retour :
        ft.Container : Conteneur contenant les composants de l'application.
    """

    # Variable pour stocker le dataset DICOM chargé
    dicom_dataset = None
    file_name = None

    # Dictionnaire pour associer les champs de l'interface utilisateur aux éléments du dataset
    field_mapping = {}

    # Conteneur défilable pour afficher les balises DICOM
    scrollable_container = create_file_explorer(page)
    #filename_text = ft.Text('', weight=ft.FontWeight.BOLD)
    
    # Conteneur pour afficher le nom du fichier chargé
    filename_container, filename_text, close_icon = create_file_name()
    divider = ft.Divider(visible=False)
    
    #Fonction pour effacer le contenu de viewer_container + désactiver le bouton de sauvegarde et d'envoi TCP/IP
    def close_file(page):
        viewer_container.content=scrollable_container #On réinitialise le contenu de viewer_container
        viewer_container.update()
        
        scrollable_container.controls.clear() #On vide le contenu de scrollable_container
        scrollable_container.update()
        
        field_mapping.clear() #On vide field_mapping
        field_mapping.update()
        
        filename_text.value = '' #On vide le nom du fichier chargé
        filename_text.update()
        
        close_icon.visible = False #On masque l'icone pour fermer le fichier chargé
        close_icon.update()
        
        divider.visible = False #On masque le divider
        divider.update()
        
        save_file_button.disabled = True #On désactive le bouton de sauvegarde
        save_file_button.update()
        
        tcp_send_button.disabled = True #On désactive le bouton d'envoi TCP/IP
        tcp_send_button.update()
        
    #Liaison de la fonction close_file au bouton close_icon
    close_icon.on_click = close_file

    # Initialisation des FilePickers pour le chargement et la sauvegarde des fichiers DICOM
    file_picker = ft.FilePicker()
    save_file_picker = ft.FilePicker()

    # Fonction pour gérer la sélection d'un fichier via le FilePicker
    def handle_file_picker_result(e):
        """
        Gestionnaire d'événements pour le FilePicker.
        Charge le fichier DICOM sélectionné et met à jour l'interface utilisateur.

        Paramètres :
            e : Événement de sélection de fichier.
        """
        nonlocal dicom_dataset  # Permet de modifier la variable `dicom_dataset` définie à l'extérieur
        nonlocal file_name # Permet de modifier la variable `file_name` définie à l'extérieur
        dicom_dataset, file_name = process_dicom_file(
            e,
            dicom_dataset,
            scrollable_container,
            filename_text,
            page,
            field_mapping
        )

        # Active ou désactive le bouton de sauvegarde en fonction de l'état de dicom_dataset
        save_file_button.disabled = dicom_dataset is None
        tcp_send_button.disabled = dicom_dataset is None
        close_icon.visible = filename_text != ''
        divider.visible = filename_text != ''
        page.update()

    # Associer la fonction de gestion au FilePicker pour le chargement
    file_picker.on_result = handle_file_picker_result

    # Fonction pour gérer la sauvegarde des modifications apportées au fichier DICOM
    save_file_picker.on_result = lambda e: save_dicom_file(
        e,
        dicom_dataset,
        field_mapping,
        page
    )

    # Ajouter les FilePickers à l'interface (en arrière-plan, overlay)
    page.overlay.extend([file_picker, save_file_picker])
    
    # Crée le menu latéral avec les boutons pour charger et sauvegarder un fichier
    menu, save_file_button, tcp_send_button = create_menu(page, file_picker, save_file_picker)

    # Crée le container pour afficher le formulaire d'envoi TCP/IP
    def handle_tcp_form(e):
        nonlocal dicom_dataset
        viewer_container.content = create_tcp_form(page, dicom_dataset)
        viewer_container.update()
    
    #fonction pour afficher la fenêtre d'envoi TCP/IP
    #def tcp_send_view(page):
    #    viewer_container.content=tcp_send_container
    #    viewer_container.update()
        
    tcp_send_button.on_click = handle_tcp_form
    
    #Container avec largeur adaptative pour afficher le nom du fichier chargé
    name_container = ft.Container(
        content=ft.Column(
            controls=[
                #Devrait être remplacé par filename_container
                ft.Row(
                    controls=[
                        filename_text,
                        ft.Container(
                            expand=True,
                        ),
                        close_icon,
                    ],
                ),
                divider,
            ],
        ),
        bgcolor=ft.colors.GREY_100,
        width=(page.width-250),
        padding=ft.padding.only(left=15, right=15, top = 15),
    )
    
    # Container avec hauteur et largeur adaptatives pour afficher le message DICOM/les interfaces TCP/IP
    viewer_container = ft.Container(
        content=scrollable_container,
        bgcolor=ft.colors.GREY_100,  # Couleur de fond du menu
        width=(page.width-250),  # Largeur fixe du menu latéral = taille de la page - la barre de navigation
        padding=15,  # Espacement interne
        alignment=ft.alignment.center,
    )
    
    #Container avec hauteur et largeur adaptatives pour afficher la view app de droite (nom du fichier + page)*
    app_container = ft.Container(
        content=ft.Column(
                controls=[
                    ft.Column(
                        controls=[
                        name_container,
                        viewer_container,
                        ],
                        spacing=0,
                    )# Conteneur défilable pour afficher le contenu DICOM
                ],
            ),
        height=page.height,  # Hauteur du conteneur ajustée à la page 
        width=(page.width-250),  # Largeur fixe du menu latéral = taille de la page - la barre de navigation
        margin=-10, # Espacement externe
    )

    # Fonction pour ajuster la taille du container lorsque la fenêtre est redimensionnée
    def on_resize(e):
        new_width = page.width - 250
        app_container.height = page.height  # Ajuste la hauteur en fonction de la hauteur de la fenêtre
        viewer_container.width = new_width  # Ajuste la largeur en fonction de la hauteur de la fenêtre
        name_container.width = new_width # Ajuste la largeur en fonction de la hauteur de la fenêtre
        page.update()  # Met à jour la page pour appliquer le changement

    # Attacher l'événement de redimensionnement à la page
    page.on_resize = on_resize
    
    # Conteneur principal structurant l'interface utilisateur
    content = ft.Row(
        controls=[
            menu,  # Menu latéral contenant les boutons d'action
            app_container,
        ],
    )

    # Retourner le conteneur principal
    return content