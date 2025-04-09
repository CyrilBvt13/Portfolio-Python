import cv2
import time
import os
from collections import deque
from ultralytics import YOLO

# === CONFIGURATION ===
RTSP_URL = "rtsp://DomoticzSafe:251193Andrea!@192.168.1.39:554/stream1"
RECORD_DURATION = 30  # secondes
OUTPUT_FOLDER = "./clips"
MODEL_PATH = "yolov8n.pt"  # ou yolov8s.pt

PRE_RECORD_SECONDS = 30
POST_RECORD_SECONDS = 30

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

# === ENREGISTREMENT ===
def start_recording():
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"{OUTPUT_FOLDER}/clip_{timestamp}.mp4"
    print(f"📹 Enregistrement démarré : {filename}")
    return cv2.VideoWriter(filename, fourcc, fps, (frame_width, frame_height)), time.time()

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

# === BOUCLE PRINCIPALE ===
while True:
    ret, frame = cap.read()
    if not ret:
        print("Erreur de lecture du flux.")
        break

    # Ajout de la frame dans le buffer circulaire
    frame_buffer.append(frame.copy())

    # Détection mouvement (simple diff)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    if 'prev_gray' not in locals():
        prev_gray = gray
        continue

    diff = cv2.absdiff(prev_gray, gray)
    prev_gray = gray.copy()
    thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
    motion_area = cv2.countNonZero(thresh)

    # S'il y a du mouvement, lancer YOLO
    person_detected = False
    results = None
    if motion_area > 10000:
        results = model(frame)[0]
        person_detected = any(int(box.cls[0]) == 0 for box in results.boxes)

    # Démarrage ou prolongement de l'enregistrement
    if person_detected:
        print(f"📹 Personne détéctée!")
        last_detection_time = time.time()
        if not recording:
            video_writer, record_start_time = start_recording()
            for buffered_frame in frame_buffer:
                add_timestamp(buffered_frame)
                video_writer.write(buffered_frame)
            recording = True

    # Si on enregistre, écrire la frame actuelle
    if recording:
        # Ajouter boxes et timestamp
        if results:
            draw_annotations(frame, results.boxes)
        add_timestamp(frame)
        video_writer.write(frame)

        # Arrêt après 30 sec sans personne détectée
        if time.time() - last_detection_time > POST_RECORD_SECONDS:
            print("🛑 Fin de l'enregistrement.")
            video_writer.release()
            recording = False
            frame_buffer.clear()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Nettoyage
cap.release()
if video_writer:
    video_writer.release()
cv2.destroyAllWindows()
