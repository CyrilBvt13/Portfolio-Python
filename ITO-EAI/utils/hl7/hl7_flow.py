import threading
import socket
import time
import requests
import hl7  # Import de la librairie HL7

BASE = "http://127.0.0.1:5000/"

class HL7Flow:
    """Classe définissant le fonctionnement d'un flux HL7 sur un thread dédié."""

    def __init__(self, flow_id, listen_port, target_ip, target_port):
        self.flow_id = flow_id
        self.listen_port = listen_port
        self.target_ip = target_ip
        self.target_port = target_port
        self.running = False
        self.thread = None
        self.server_socket = None  

    def start(self):
        """Démarre le flux HL7 si son état en base est actif."""
        if not self.running and self.is_active_in_db():
            self.running = True
            self.thread = threading.Thread(target=self.run, daemon=True)
            self.thread.start()
            print(f"✅ Flow {self.flow_id} started.")

    def stop(self):
        """Arrête le flux HL7 et ferme la socket proprement."""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
            self.server_socket = None
        if self.thread:
            self.thread.join()
            print(f"⛔ Flow {self.flow_id} stopped.")

    def run(self):
        """Gère la réception et l'envoi des messages HL7."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.server_socket:
            try:
                self.server_socket.bind(("0.0.0.0", self.listen_port))
                self.server_socket.listen(5)
                self.server_socket.settimeout(1.0)
                print(f"🚀 Flow {self.flow_id} listening on port {self.listen_port}")

                while self.running:
                    try:
                        client_socket, addr = self.server_socket.accept()
                        with client_socket:
                            data = self.receive_hl7_message(client_socket)

                            if data:
                                print(f"📩 Received HL7 message:\n{data}")

                                if not self.is_valid_hl7(data):
                                    print(f"⚠️ Invalid HL7 message in flow {self.flow_id}")
                                    #client_socket.sendall(b"Error: Invalid HL7 format")
                                    continue

                                transformed_data = self.transform_hl7(data)
                                self.send_to_target(transformed_data)

                                ack_message = self.generate_hl7_ack(data)
                                client_socket.sendall(ack_message.encode("utf-8"))
                                print(f"✅ Sent ACK for flow {self.flow_id}")

                    except socket.timeout:
                        continue  
                    except Exception as e:
                        print(f"❌ Error in flow {self.flow_id}: {e}")

            except Exception as e:
                print(f"❌ Failed to start flow {self.flow_id} on port {self.listen_port}: {e}")

    def receive_hl7_message(self, client_socket):
        """Lit un message HL7 en respectant les délimiteurs \x0b et \x1c\x0d, et prépare un message valide pour hl7.parse()."""
        buffer = b""
    
        while True:
            chunk = client_socket.recv(1024)
            if not chunk:
                break
            buffer += chunk
            if b"\x1c\x0d" in buffer:  # Fin de message HL7 détectée
                break
    
        # Décodage en UTF-8
        message = buffer.decode("utf-8", errors="replace").strip()

        return message


    def is_valid_hl7(self, message):
        """Vérifie si le message HL7 est valide."""
        try:
            parsed = hl7.parse(message)
            return str(parsed[0][0]) == "MSH" 
        except Exception as e:
            print(f"⚠️ Erreur de parsing HL7 : {e}")
            return False

    def transform_hl7(self, message):
        """Transformation HL7 (exemple : modification d’un champ)."""
        try:
            print('🔄 Transformation du message...')
            # + Récupèrer les infos en bd
            parsed = hl7.parse(message)
            if "PID" in repr(parsed):
                print(parsed.segment("PID")[5][0])
                parsed.segment("PID")[5][0] = "MODIFIED_NAME"
            return str(parsed)
        except Exception as e:
            print(f"⚠️ Error transforming HL7 message: {e}")
            return message

    def send_to_target(self, message):
        """Envoie le message HL7 transformé vers la cible."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((self.target_ip, self.target_port))
                hl7_message = f"\x0b{message}\x1c\x0d"
                sock.sendall(hl7_message.encode("utf-8"))
                print(f"📤 Sent HL7 message to {self.target_ip}:{self.target_port}\n{hl7_message}")
        except Exception as e:
            print(f"❌ Error sending data in flow {self.flow_id}: {e}")

    def generate_hl7_ack(self, message):
        """Génère un message ACK HL7 avec la bibliothèque hl7."""
        try:
            parsed = hl7.parse(message)
            message_control_id = parsed.segment("MSH")[10][0] if "MSH" in repr(parsed) else "UNKNOWN"
            
            ack_message = f"MSH|^~\&|ACK_SYSTEM|{self.flow_id}|||ACK|\rMSA|AA|{message_control_id}"

            return f"\x0b{str(ack_message)}\x1c\x0d"
        except Exception as e:
            print(f"⚠️ Error generating HL7 ACK: {e}")
            return "\x0bMSH|^~\\&|ACK_SYSTEM|UNKNOWN||UNKNOWN|ACK\rMSA|AE|ERROR\r\x1c\x0d"

    def is_active_in_db(self):
        """Vérifie si le flux est actif en base."""
        try:
            response = requests.get(BASE + f"flow/{self.flow_id}", json={})
            if response.status_code == 200:
                return response.json()[0].get('flow_is_active', False)
        except Exception as e:
            print(f"❌ Error fetching flow status from DB: {e}")
        return False

flows = {}

def start_flow(flow_id, listen_port, target_ip, target_port):
    if flow_id not in flows:
        flows[flow_id] = HL7Flow(flow_id, listen_port, target_ip, target_port)
    flows[flow_id].start()

def stop_flow(flow_id):
    if flow_id in flows:
        flows[flow_id].stop()
        del flows[flow_id]

def load_active_flows():
    """Fonction pour charger les flux actifs au démarrage de l'application"""
    print("🔄 Démarrage des flux...")
    
    try:
        #Pour chaque groupe on récupère la liste des flux
        response = requests.get(BASE + "groups/", json={})

        if response.status_code == 200:
            groups = response.json().get("groups", [])

            # Parcourir les groupes et créer des boutons pour chacun
            for group in groups:
                group_id = group.get("group_id", "")
                response = requests.get(BASE + "flows/" + group_id, json={})
                if response.status_code == 200:
                    flows = response.json().get("flows", [])
                    for flow in flows:
                        flow_id = flow.get('flow_id')                      
                        if flow.get('flow_is_active'):
                            #start_flow(flow['flow_id'], flow['listen_port'], flow['target_ip'], flow['target_port']) # + Récupèrer les infos en bd
                            start_flow(flow['flow_id'], 6000, '127.0.0.1', 6001)

    except Exception as e:
        print(f"❌ Error loading active flows from DB: {e}")