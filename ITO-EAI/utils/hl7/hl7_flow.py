import threading
import socket

class HL7Flow:
    """
    Gère la réception, transformation et transmission des messages HL7.
    """

    def __init__(self, flow_id, listen_port, target_ip, target_port):
        self.flow_id = flow_id
        self.listen_port = listen_port
        self.target_ip = target_ip
        self.target_port = target_port
        self.running = False
        self.thread = None

    def start(self):
        """Démarre le flux HL7."""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.run, daemon=True)
            self.thread.start()
            print(f"✅ Flow {self.flow_id} started.")

    def stop(self):
        """Arrête le flux HL7."""
        self.running = False
        if self.thread:
            self.thread.join()
            print(f"⛔ Flow {self.flow_id} stopped.")

    def run(self):
        """Gère la réception et l'envoi des messages HL7."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            try:
                server_socket.bind(("0.0.0.0", self.listen_port))
                server_socket.listen(5)
                print(f"🚀 Flow {self.flow_id} listening on port {self.listen_port}")

                while self.running:
                    try:
                        client_socket, addr = server_socket.accept()
                        with client_socket:
                            data = self.receive_hl7_message(client_socket)
                            
                            if data:
                                print(f"📩 Received HL7 message:\n{data}")

                                # Vérification format HL7
                                if not data.startswith("MSH"):
                                    print(f"⚠️ Bad HL7 format received in flow {self.flow_id}")
                                    client_socket.sendall(b"Error: Bad HL7 format")
                                    continue

                                # Transformation du message HL7
                                transformed_data = self.transform_hl7(data)

                                # Envoi vers la cible
                                self.send_to_target(transformed_data)

                                # Envoi de l'ACK HL7
                                ack_message = self.generate_hl7_ack(data)
                                client_socket.sendall(ack_message.encode("utf-8"))
                                print(f"✅ Sent ACK for flow {self.flow_id}")

                    except Exception as e:
                        print(f"❌ Error in flow {self.flow_id}: {e}")

            except Exception as e:
                print(f"❌ Failed to start flow {self.flow_id} on port {self.listen_port}: {e}")

    def receive_hl7_message(self, client_socket):
        """Lit un message HL7 en respectant les délimiteurs \x0b (début) et \x1c\x0d (fin)."""
        buffer = b""
        while True:
            chunk = client_socket.recv(1024)
            if not chunk:
                break
            buffer += chunk
            if b"\x1c\x0d" in buffer:  # Fin de message détectée
                break
        message = buffer.decode("utf-8").strip()
        
        # Suppression des délimiteurs HL7 (\x0b au début et \x1c\x0d à la fin)
        if message.startswith("\x0b"):
            message = message[1:]
        if message.endswith("\x1c\x0d"):
            message = message[:-2]

        return message

    def transform_hl7(self, message):
        """Transformation HL7 (exemple : mise en majuscules)."""
        return message.upper()

    def send_to_target(self, message):
        """Envoie le message HL7 transformé vers la cible."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((self.target_ip, self.target_port))
                hl7_message = f"\x0b{message}\x1c\x0d"
                sock.sendall(hl7_message.encode("utf-8"))
                print(f"📤 Sent HL7 message to {self.target_ip}:{self.target_port}")
        except Exception as e:
            print(f"❌ Error sending data in flow {self.flow_id}: {e}")

    def generate_hl7_ack(self, message):
        """Génère un message ACK HL7 en respectant la structure HL7."""
        return "\x0bMSH|^~\\&|ACK_SYSTEM|{self.flow_id}||{self.target_ip}|ACK\rMSA|AA|{self.flow_id}\r\x1c\x0d"

# Liste des flux actifs à stocker en bd
flows = {}

def start_flow(flow_id, listen_port, target_ip, target_port):
    """Démarre un flux HL7."""
    if flow_id not in flows:
        flows[flow_id] = HL7Flow(flow_id, listen_port, target_ip, target_port)
        flows[flow_id].start()

def stop_flow(flow_id):
    """Arrête un flux HL7."""
    if flow_id in flows:
        print(f"⛔ Stopping flow {flow_id}...")
        flows[flow_id].stop()
        del flows[flow_id]
    else:
        print(f"❌ Error stopping flow {flow_id}")