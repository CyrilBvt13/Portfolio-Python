def readConf():
    """
    Lit les variables de configuration depuis un fichier 'config.txt'.
    Les variables reconnues sont :
    - target : Adresse cible ou hôte
    - input_port : Port d'écoute
    - output_port : Port d'émission
    - log_mode : Activation de l'écriture des logs

    Retourne :
        tuple : (target, input_port, output_port, log_mode) contenant les valeurs des paramètres lues.
    """
    variables = {}

    # Valeurs par défaut
    target = ''
    input_port = '1'
    output_port = '1'
    log_mode = 0

    # Ouverture du fichier de configuration pour lecture
    with open('config.txt', 'r') as fichier:
        lignes = fichier.readlines()
        for ligne in lignes:
            # Ignorer les lignes vides ou les commentaires
            if ligne.strip() == '' or ligne.strip().startswith('#'):
                continue
            # Extraction du nom de la variable et de sa valeur
            nom_variable, valeur = ligne.strip().split('=')
            variables[nom_variable.strip()] = valeur.strip()

    # Parcourir les variables extraites pour attribuer les valeurs correspondantes
    for nom_variable, valeur in variables.items():
        if nom_variable == 'target':
            target = valeur
        elif nom_variable == 'input_port':
            input_port = valeur
        elif nom_variable == 'output_port':
            output_port = valeur
        elif nom_variable == 'log_mode':
            log_mode = int(valeur)
        else:
            # Gestion des variables non reconnues
            print('Variable non reconnue:', nom_variable)

    return target, input_port, output_port, log_mode


def writeConf(target, input_port, output_port, log_mode):
    """
    Met à jour les variables de configuration dans le fichier 'config.txt'.
    Les valeurs des paramètres sont remplacées si elles existent.

    Paramètres :
        target (str) : Adresse cible ou hôte
        input_port (int) : Port d'écoute
        output_port (int) : Port d'émission
        log_mode (bool) : Activation de l'écriture des logs
    """
    # Lire le fichier de configuration existant
    with open('config.txt', 'r') as file:
        lines = file.readlines()

    # Mise à jour des lignes correspondant aux variables
    for i, line in enumerate(lines):
        if line.startswith('target='):
            lines[i] = f'target={target}\n'
        elif line.startswith('input_port='):
            lines[i] = f'input_port={input_port}\n'
        elif line.startswith('output_port='):
            lines[i] = f'output_port={output_port}\n'
        elif line.startswith('log_mode='):
            lines[i] = f'log_mode={log_mode}\n'

    # Réécriture du fichier de configuration avec les nouvelles valeurs
    with open('config.txt', 'w') as file:
        file.writelines(lines)