import threading
import time

def execute_flow(flow):
    """
    Simule l'exécution d'un flux.
    """
    print(f"[{flow['flow_name']}] Démarrage du flux...")
    receivers = flow["flow_receivers"]
    transformers = flow["flow_transformers"]
    senders = flow["flow_senders"]
    
    # Exécuter les receveurs
    for receiver in receivers:
        print(f"[{flow['flow_name']}] Receveur actif : {receiver['receiver_name']}")
    
    # Exécuter les transformateurs
    for transformer in transformers:
        print(f"[{flow['flow_name']}] Transformateur actif : {transformer['transformer_name']}")
        for rule in transformer["transformer_rules"]:
            print(f"[{flow['flow_name']}] Appliquer la règle : {rule['rule_name']}")
    
    # Exécuter les expéditeurs
    for sender in senders:
        print(f"[{flow['flow_name']}] Expéditeur actif : {sender['sender_name']}")
    
    print(f"[{flow['flow_name']}] Flux terminé.")

def launch_flows_in_threads(flows):
    """
    Lance chaque flux dans un thread distinct.
    """
    threads = []
    for flow in flows:
        thread = threading.Thread(target=execute_flow, args=(flow,))
        threads.append(thread)
        thread.start()

    # Attendre la fin de tous les threads
    for thread in threads:
        thread.join()