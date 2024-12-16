def transform_message(message):
    """
    Fonction pour transformer un message HL7 en modifiant les segments selon des règles prédéfinies.

    Paramètre :
        message : Objet HL7 contenant les segments à modifier.

    Retourne :
        modified_message : Liste contenant les segments HL7 modifiés sous forme de chaînes.
    """

    # Extraction et modification du segment MSH
    MSHField = []
    for i in range(0, len(message.segment('MSH'))):
        MSHField.append(message.segment('MSH')(i))

    # Inversion des champs entre émetteur et récepteur
    MSH3 = MSHField[3]  # Application ID (Source)
    MSH4 = MSHField[4]  # Facility ID (Source)
    MSH5 = MSHField[5]  # Application ID (Destination)
    MSH6 = MSHField[6]  # Facility ID (Destination)

    MSHField[3] = MSH5
    MSHField[4] = MSH6
    MSHField[5] = MSH3
    MSHField[6] = MSH4

    # Modification de l'événement message type
    MSHField[9] = 'ORL^O22^ORL_O22'

    # Reconstruction du segment MSH sous forme de chaîne
    MSH = 'MSH|^~\&'
    for i in range(3, len(MSHField)):
        MSH += '|' + str(MSHField[i])

    # Modification et reconstruction du segment MSA
    MSA = 'MSA|AA|' + str(message.segment('MSH')(10))  # Ajout de l'ACK Code (Segment MSH, champ 10)

    # Modification et reconstruction du segment PID
    PIDField = []
    for i in range(0, len(message.segment('PID'))):
        PIDField.append(message.segment('PID')(i))

    PID = 'PID'
    for i in range(1, len(PIDField)):
        PID += '|' + str(PIDField[i])

    # Modification et reconstruction du segment ORC
    ORCField = []
    for i in range(0, len(message.segment('ORC'))):
        ORCField.append(message.segment('ORC')(i))

    ORCField[3] = ORCField[2]  # Réplication de la valeur du champ ORC-2 dans ORC-3

    ORC = 'ORC'
    for i in range(1, len(ORCField)):
        ORC += '|' + str(ORCField[i])

    # Reconstruction du segment TQ1 sans modification des champs
    TQ1Field = []
    for i in range(0, len(message.segment('TQ1'))):
        TQ1Field.append(message.segment('TQ1')(i))

    TQ1 = 'TQ1'
    for i in range(1, len(TQ1Field)):
        TQ1 += '|' + str(TQ1Field[i])

    # Modification et reconstruction du segment OBR
    OBRField = []
    for i in range(0, len(message.segment('OBR'))):
        OBRField.append(message.segment('OBR')(i))

    OBRField[3] = OBRField[2]  # Réplication de la valeur du champ OBR-2 dans OBR-3

    OBR = 'OBR'
    for i in range(1, len(OBRField)):
        OBR += '|' + str(OBRField[i])

    # Modification et reconstruction du segment SPM
    SPMField = []
    for i in range(0, len(message.segment('SPM'))):
        SPMField.append(message.segment('SPM')(i))

    # Modification des champs spécifiques dans SPM
    SPMField[4] = 'HEPLI^Tube Héparinate de Lithium^L'
    SPMField[27] = '^Tube 4ml vert avec gel (Héparinate Li)^L'

    SPM = 'SPM'
    for i in range(1, len(SPMField)):
        SPM += '|' + str(SPMField[i])

    # Liste des segments HL7 modifiés
    modified_message = [MSH, MSA, PID, ORC, TQ1, OBR, SPM]

    return modified_message