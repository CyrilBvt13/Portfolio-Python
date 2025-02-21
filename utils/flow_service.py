import socket
import sys
import hl7_transformer
import threading

"""
    Mode d'emploi : ces fonctions permettent le fonctionnement des flux en mode service. 
    
    Elles sont appel�es par services/service_manager.py
"""

def handle_client(client_socket, ip_target, port_target):
    """G�re la connexion avec un client et envoie le message transform�."""
    try:
        data = client_socket.recv(1024)
        if data:
            transformed_message = hl7_transformer.transform(data.decode("utf-8"))
            send_to_target(ip_target, port_target, transformed_message)
    finally:
        client_socket.close()

def start_service(flow_id):
    """D�marre un serveur TCP dans un thread pour g�rer le flux."""
    # Simulation des param�tres du flux (en production, � r�cup�rer depuis une base de donn�es)
    port_listen = 5000  # Port unique pour chaque flux
    ip_target = "127.0.0.1"  # IP cible
    port_target = 6000  # Port cible

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", port_listen))
    server_socket.listen(5)

    print(f"[Flux {flow_id}] Service d�marr� sur le port {port_listen}")

    while True:
        client_socket, _ = server_socket.accept()
        # D�marre un thread pour chaque connexion entrante
        client_thread = threading.Thread(target=handle_client, args=(client_socket, ip_target, port_target))
        client_thread.start()

def send_to_target(ip, port, message):
    """Envoie un message HL7 transform� vers l'IP cible."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((ip, port))
        client_socket.sendall(message.encode("utf-8"))

if __name__ == "__main__":
    flow_id = sys.argv[1]
    thread = threading.Thread(target=start_service, args=(flow_id,))
    thread.start()