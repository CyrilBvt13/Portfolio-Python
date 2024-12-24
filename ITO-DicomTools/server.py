import threading
import socket
from dicom_handler import process_dicom_file

# Fonction pour démarrer le serveur TCP/IP
def start_tcp_server(
    page, 
    dicom_dataset, 
    scrollable_container, 
    field_mapping, 
    save_file_button,
    tcp_send_button,
    host, 
    port):
    
    def tcp_server():
        nonlocal dicom_dataset

        buffer_size = 4096

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((host, port))
            server_socket.listen(1)
            print("Serveur TCP en écoute sur le port", port)
            while True:
                client_socket, addr = server_socket.accept()
                with client_socket:
                    print(f"Connexion établie avec {addr}")
                    data = client_socket.recv(buffer_size)
                    if data:
                        # Simule un fichier temporaire pour traiter les données reçues
                        e = {"path": None, "data": data}
                        dicom_dataset, file_name = process_dicom_file(
                            e,
                            dicom_dataset,
                            scrollable_container,
                            page,
                            field_mapping
                        )
                        save_file_button.disabled = dicom_dataset is None #True (masqué) si dicom_dataset et vide sinon False (visible)
                        tcp_send_button.disabled = dicom_dataset is None #True (masqué) si dicom_dataset et vide sinon False (visible)
                        page.update()

    # Lancer le serveur TCP dans un thread séparé
    server_thread = threading.Thread(target=tcp_server, daemon=True)
    server_thread.start()