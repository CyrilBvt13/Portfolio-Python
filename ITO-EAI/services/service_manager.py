import sys
import subprocess
import os

SCRIPT_PATH = os.path.abspath("flow_service.py")

"""
    Mode d'emploi : ces fonctions permettent l'installation, le d�marrage et l'arr�t de services windows pour chaque flux.

    # Cr�ation du service Windows :
        subprocess.run(["python", "services/service_manager.py", "install", str(flow_id)])

    # D�marrer ou arr�ter le service Windows associ� :
        if is_active:
            subprocess.run(["python", "service_manager.py", "stop", str(flow_id)])
        else:
            subprocess.run(["python", "service_manager.py", "start", str(flow_id)])

    Ces fonctions font appel au fichier utils/flow_service.py
"""

def install_service(flow_id):
    """Installe le service Windows pour un flux donn�."""
    service_name = f"FlowService_{flow_id}"
    cmd = f'nssm install {service_name} "python" "flow_service.py {flow_id}"'
    subprocess.run(cmd, shell=True)
    #subprocess.run(f'nssm start {service_name}', shell=True)
    print(f"Service {service_name} install�.")

def start_service(flow_id):
    """D�marre un service existant."""
    service_name = f"FlowService_{flow_id}"
    subprocess.run(f'nssm start {service_name}', shell=True)

def stop_service(flow_id):
    """Arr�te un service."""
    service_name = f"FlowService_{flow_id}"
    subprocess.run(f'nssm stop {service_name}', shell=True)

if __name__ == "__main__":
    action = sys.argv[1]
    flow_id = sys.argv[2]

    if action == "install":
        install_service(flow_id)
    elif action == "start":
        start_service(flow_id)
    elif action == "stop":
        stop_service(flow_id)