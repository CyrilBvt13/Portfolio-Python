#!/bin/bash

echo "🚨 Lancement de toutes les caméras de surveillance..."

# Dossier de logs
mkdir -p logs

# Lancement de chaque caméra dans un terminal en arrière-plan
python surveillance/camera1.py > logs/camera1.log 2>&1 &
echo "✅ camera1.py lancé (PID $!)"

#python surveillance/camera2.py > logs/camera2.log 2>&1 &
#echo "✅ camera2.py lancé (PID $!)"

#python surveillance/camera3.py > logs/camera3.log 2>&1 &
#echo "✅ camera3.py lancé (PID $!)"

echo "🎥 Toutes les caméras sont en cours d'exécution."

#chmod +x run_all_cameras.sh stop_all.sh