import cv2
import time
import os
import smtplib
import zipfile
import numpy as np
from email.message import EmailMessage
from collections import deque
from ultralytics import YOLO

# === CONFIGURATION ===
RTSP_URL = "rtsp://DomoticzSafe:251193Andrea!@192.168.1.39:554/stream1"
CAMERA_NAME = "Jardin Derrière"
OUTPUT_FOLDER = "./clips"
MODEL_PATH = "yolov8n.pt"

PRE_RECORD_SECONDS = 10
POST_RECORD_SECONDS = 20

SENDER_EMAIL = "lefablabdecyril@gmail.com"
SENDER_PASSWORD = "tfvedxhrgrhweuww"
RECIPIENT_EMAILS = ["cyril.bouvart@gmail.com"]
#RECIPIENT_EMAILS = ["cyril.bouvart@gmail.com", "cimino.andrea25@gmail.com"]

# === INITIALISATION ===
model = YOLO(MODEL_PATH)
cap = cv2.VideoCapture(RTSP_URL)
fps = int(cap.get(cv2.CAP_PROP_FPS)) or 25
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

frame_buffer = deque(maxlen=PRE_RECORD_SECONDS * fps)
recording = False
last_detection_time = 0
video_writer = None
video_filename = ""
last_obstruction_check = 0
obstruction_cooldown = 3600  # secondes entre deux mails d'obstruction

# === FONCTIONS ===

def zip_file(source_path):
    zip_path = source_path.replace(".mp4", ".zip")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(source_path, os.path.basename(source_path))
    return zip_path

def send_email_with_attachment(zip_path):
    try:
        print("📬 Envoi du clip compressé par e-mail...")
        msg = EmailMessage()
        msg["Subject"] = f"📹 {CAMERA_NAME.upper()} - Détection de personne"
        msg["From"] = SENDER_EMAIL
        msg["To"] = ", ".join(RECIPIENT_EMAILS)
        msg.set_content("Une personne a été détectée. Le clip est compressé en pièce jointe.")

        with open(zip_path, "rb") as f:
            # Ajouter une vérification de taille de fichier
            file_data = f.read()
            file_name = os.path.basename(zip_path)
            #msg.add_attachment(file_data, maintype="application", subtype="zip", filename=file_name)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        print("✅ Clip envoyé aux destinataires.")
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi de l'e-mail : {e}")

def send_obstruction_email(camera_name):
    try:
        msg = EmailMessage()
        msg["Subject"] = f"🚫 {camera_name.upper()} - Caméra possiblement obstruée"
        msg["From"] = SENDER_EMAIL
        msg["To"] = ", ".join(RECIPIENT_EMAILS)
        msg.set_content(f"⚠️ La caméra '{camera_name}' semble obstruée ou retournée.")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        print(f"📧 Alerte obstruction envoyée pour {camera_name}.")
    except Exception as e:
        print(f"❌ Erreur d'envoi de l'alerte obstruction : {e}")

def start_recording():
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"{OUTPUT_FOLDER}/{CAMERA_NAME}_{timestamp}.mp4"
    print(f"📹 Enregistrement démarré : {filename}")
    return cv2.VideoWriter(filename, fourcc, fps, (frame_width, frame_height)), filename, time.time()

def draw_annotations(frame, boxes):
    for box in boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        if cls_id == 0:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = f"Person {conf:.2f}"
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

def add_timestamp(frame):
    now_str = time.strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(frame, f"Timestamp: {now_str}", (10, frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

def is_camera_obstructed(frame, threshold=10):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    std_dev = np.std(gray)
    return std_dev < threshold  # Très peu de variations → image "plate"

# === BOUCLE PRINCIPALE ===
while True:
    ret, frame = cap.read()
    if not ret:
        print("Erreur de lecture du flux.")
        break

    frame_buffer.append(frame.copy())

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    if 'prev_gray' not in locals():
        prev_gray = gray
        continue

    diff = cv2.absdiff(prev_gray, gray)
    prev_gray = gray.copy()
    thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
    motion_area = cv2.countNonZero(thresh)

    person_detected = False
    results = None
    if motion_area > 10000:
        results = model(frame)[0]
        person_detected = any(int(box.cls[0]) == 0 for box in results.boxes)

    if person_detected:
        last_detection_time = time.time()
        if not recording:
            video_writer, video_filename, record_start_time = start_recording()
            for buffered_frame in frame_buffer:
                add_timestamp(buffered_frame)
                video_writer.write(buffered_frame)
            recording = True

    if recording:
        if results:
            draw_annotations(frame, results.boxes)
        add_timestamp(frame)
        video_writer.write(frame)

        if time.time() - last_detection_time > POST_RECORD_SECONDS:
            print("🛑 Fin de l’enregistrement.")
            video_writer.release()
            recording = False
            frame_buffer.clear()

            # ➤ Compression
            zip_path = zip_file(video_filename)

            # ➤ Envoi par e-mail
            send_email_with_attachment(zip_path)

            # ➤ Suppression locale
            try:
                #os.remove(video_filename)
                os.remove(zip_path)
                print("🗑️ Fichier zip supprimé après envoi.")
            except Exception as e:
                print(f"Erreur suppression fichier : {e}")
    
    current_time = time.time()

    # Vérification toutes les 5 secondes
    if current_time - last_obstruction_check > 5:
        if is_camera_obstructed(frame) and (current_time - last_detection_time > POST_RECORD_SECONDS):
            print("⚠️ Caméra potentiellement obstruée.")

            if current_time - last_obstruction_check > obstruction_cooldown:
                send_obstruction_email(CAMERA_NAME)
                last_obstruction_check = current_time

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
if video_writer:
    video_writer.release()
cv2.destroyAllWindows()