import flet as ft
from flet import Text, TextField, ElevatedButton, Container
from flet_core import ControlEvent

from hl7server import startServer, getIsStarted, setIsStarted
from config import readConf, writeConf
from log import log

# Fonction principale pour la création de l'interface utilisateur de l'application
def AppView(page):
    """
    Crée l'interface utilisateur pour la configuration et le contrôle d'un serveur HL7.
    Paramètres :
        page (ft.Page) : Objet représentant la page de l'application.
    Retour :
        content (ft.Container) : Conteneur contenant tous les éléments de l'interface utilisateur.
    """

    # Chargement de la configuration depuis un fichier de configuration
    host = str(readConf()[0])  # Adresse de destination
    listport = int(readConf()[1])  # Port d'écoute
    sendport = int(readConf()[2])  # Port d'émission
    logmode = int(readConf()[3])  # Mode d'écriture des logs

    # Style des boutons
    btn_connexion_style = ft.ButtonStyle(
        shape={
            ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=5),  # Bords arrondis
        },
        bgcolor=ft.colors.GREY_200,  # Couleur d'arrière-plan
        color=ft.colors.BLACK  # Couleur du texte
    )

    # Champ de texte pour l'adresse de destination
    txtfld_host: TextField = TextField(
        hint_text="Destination",
        icon=ft.icons.COMPUTER,
        border=ft.InputBorder.NONE,
        value=host,
        disabled=False,
        width=270
    )

    # Conteneur du champ de texte pour l'adresse de destination
    txtfld_host_cont: Container = Container(
        content=txtfld_host,
        alignment=ft.alignment.center,
        width=300,
        bgcolor=ft.colors.GREY_200,
        border_radius=5
    )

    # Champ de texte pour le port d'écoute
    txtfld_listport: TextField = TextField(
        hint_text="Port d'écoute",
        value=listport,
        icon=ft.icons.LOGIN,
        border=ft.InputBorder.NONE,
        disabled=False,
        width=270
    )

    # Conteneur du champ de texte pour le port d'écoute
    txtfld_listport_cont: Container = Container(
        content=txtfld_listport,
        alignment=ft.alignment.center,
        width=300,
        bgcolor=ft.colors.GREY_200,
        border_radius=5
    )

    # Champ de texte pour le port d'émission
    txtfld_sendport: TextField = TextField(
        hint_text="Port d'émission",
        value=sendport,
        icon=ft.icons.LOGOUT,
        border=ft.InputBorder.NONE,
        disabled=False,
        width=270
    )

    # Conteneur du champ de texte pour le port d'émission
    txtfld_sendport_cont: Container = Container(
        content=txtfld_sendport,
        alignment=ft.alignment.center,
        width=300,
        bgcolor=ft.colors.GREY_200,
        border_radius=5
    )

    # Bouton pour démarrer ou arrêter le serveur
    btn_connexion: ElevatedButton = ElevatedButton(
        content=Text("Démarrer", style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
        height=40,
        width=140,
        style=btn_connexion_style
    )

    # Conteneur du bouton de connexion
    btn_connexion_cont: Container = Container(
        content=btn_connexion,
        alignment=ft.alignment.center,
        width=300
    )

    # Fonction asynchrone pour arrêter le serveur
    async def btn_stop(e: ControlEvent) -> None:
        """
        Arrête le serveur HL7 et réactive les champs de saisie.
        """
        isStarted = await getIsStarted()
        if isStarted:
            txtfld_host.disabled = False
            txtfld_listport.disabled = False
            txtfld_sendport.disabled = False
            e.control.content = Text("Démarrer", style=ft.TextStyle(weight=ft.FontWeight.BOLD))
            e.control.on_click = btn_start
            await page.update_async()
            await setIsStarted(False)
            log('Arrêt du serveur...')

    # Fonction asynchrone pour démarrer le serveur
    async def btn_start(e: ControlEvent) -> None:
        """
        Démarre le serveur HL7 et désactive les champs de saisie.
        """
        isStarted = await getIsStarted()
        if not isStarted:
            txtfld_host.disabled = True
            txtfld_listport.disabled = True
            txtfld_sendport.disabled = True
            e.control.content = Text("Stopper", style=ft.TextStyle(weight=ft.FontWeight.BOLD))
            e.control.on_click = btn_stop
            await page.update_async()
            log('Lancement du serveur...')
            await setIsStarted(True)
            while await getIsStarted():
                await startServer()

    # Mise à jour de la configuration lorsqu'une valeur change
    async def host_changed(e):
        writeConf(txtfld_host.value, listport, sendport, logmode)

    async def listport_changed(e):
        writeConf(host, txtfld_listport.value, sendport, logmode)

    async def sendport_changed(e):
        writeConf(host, listport, txtfld_sendport.value, logmode)

    # Liaison des événements
    btn_connexion.on_click = btn_start
    txtfld_host.on_change = host_changed
    txtfld_listport.on_change = listport_changed
    txtfld_sendport.on_change = sendport_changed

    # Construction de l'interface utilisateur principale
    content = Container(
        ft.Column(
            controls=[
                ft.Column(controls=[txtfld_host_cont]),
                ft.Column(controls=[txtfld_listport_cont]),
                ft.Column(controls=[txtfld_sendport_cont]),
                Container(height=10),
                ft.Column(controls=[btn_connexion_cont])
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

    return content