import socket
import paramiko

def send_tcp(data, host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(data.encode())
    except Exception as e:
        print(f"Erreur TCP : {e}")

def send_sftp(file_path, remote_path, host, port, username, password):
    try:
        transport = paramiko.Transport((host, port))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put(file_path, remote_path)
        sftp.close()
        transport.close()
    except Exception as e:
        print(f"Erreur SFTP : {e}")