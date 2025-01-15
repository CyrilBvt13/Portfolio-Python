import socketserver
import threading
from hl7_processing import process_hl7_message
from tcp_client import send_hl7_message

#Exemple pour un flux HL7
class HL7FlowServer(socketserver.ThreadingTCPServer):
    """
    Un serveur HL7 d�di� � un flux sp�cifique.
    Chaque instance g�re un port et un ensemble de r�gles.
    """

    def __init__(self, host, port, rules, client_host, client_port):
        super().__init__((host, port), HL7RequestHandler)
        self.rules = rules
        self.client_host = client_host
        self.client_port = client_port


class HL7RequestHandler(socketserver.BaseRequestHandler):
    """
    G�re les requ�tes TCP re�ues par le serveur HL7.
    """

    def handle(self):
        # Lire les donn�es entrantes (message HL7)
        raw_message = self.request.recv(1024).strip().decode("utf-8")
        print(f"Message re�u : {raw_message}")

        # Traiter le message (transformation HL7)
        modified_message = process_hl7_message(raw_message, self.server.rules)

        # Transmettre le message modifi� via TCP/IP
        send_hl7_message(modified_message, self.server.client_host, self.server.client_port)

        # R�pondre � l'�metteur d'origine
        self.request.sendall(b"Message re�u et transmis.\n")

'''
Pour lancer un flux :

import threading
from tcp_server import HL7FlowServer

def start_hl7_flow(host, port, rules, client_host, client_port):
    server = HL7FlowServer(host, port, rules, client_host, client_port)
    with server:
        print(f"Flux HL7 d�marr� sur {host}:{port}")
        server.serve_forever()

if __name__ == "__main__":
    # D�finition des flux
    flows = [
        {"host": "0.0.0.0", "port": 12345, "rules": "rules1.json", "client_host": "127.0.0.1", "client_port": 23456},
        {"host": "0.0.0.0", "port": 12346, "rules": "rules2.json", "client_host": "127.0.0.1", "client_port": 23457},
    ]

    threads = []
    for flow in flows:
        # Charger les r�gles sp�cifiques � chaque flux
        rules = load_rules(flow["rules"])

        # D�marrer un thread pour chaque flux
        t = threading.Thread(target=start_hl7_flow, args=(flow["host"], flow["port"], rules, flow["client_host"], flow["client_port"]))
        t.start()
        threads.append(t)

    # Attendre la fin de tous les threads
    for t in threads:
        t.join()
'''