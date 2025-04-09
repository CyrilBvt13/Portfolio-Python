from flask import Flask
import subprocess
import os
import signal

# Script à lancer au démarrage du serveur

app = Flask(__name__)
surveillance_process = None

RUN_SCRIPT = "./start_all.sh"
STOP_SCRIPT = "./stop_all.sh"

@app.route('/start')
def start_surveillance():
    global surveillance_process
    if surveillance_process is None:
        surveillance_process = subprocess.Popen(["bash", RUN_SCRIPT])
        return "🎬 Surveillance multi-caméras démarrée."
    else:
        return "✅ Surveillance déjà active."

@app.route('/stop')
def stop_surveillance():
    global surveillance_process
    if surveillance_process:
        subprocess.call(["bash", STOP_SCRIPT])
        os.kill(surveillance_process.pid, signal.SIGTERM)
        surveillance_process = None
        return "🛑 Surveillance arrêtée pour toutes les caméras."
    else:
        return "ℹ️ Aucune surveillance en cours."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)