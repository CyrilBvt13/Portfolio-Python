import cv2
import time
import os
from ultralytics import YOLO

# === CONFIGURATION ===
RTSP_URL = "rtsp://DomoticzSafe:251193Andrea!@192.168.1.39:554/stream1"
RECORD_DURATION = 30  # secondes
OUTPUT_FOLDER = "./clips"
MODEL_PATH = "yolov8n.pt"  # ou yolov8s.pt

# === INITIALISATION ===
model = YOLO(MODEL_PATH)
cap = cv2.VideoCapture(RTSP_URL)
fps = int(cap.get(cv2.CAP_PROP_FPS)) or 25
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")

# Préparer le dossier
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Variables de détection de mouvement
ret, prev_frame = cap.read()
prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
prev_gray = cv2.GaussianBlur(prev_gray, (21, 21), 0)

motion_detected = False
recording = False
record_start_time = 0
video_writer = None

# === FONCTION ENREGISTREMENT ===
def start_recording():
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"{OUTPUT_FOLDER}/clip_{timestamp}.mp4"
    print(f"📹 Enregistrement démarré : {filename}")
    return cv2.VideoWriter(filename, fourcc, fps, (frame_width, frame_height)), time.time()

# === BOUCLE PRINCIPALE ===
while True:
    ret, frame = cap.read()
    if not ret:
        print("Erreur de lecture du flux.")
        break

    # Détection de mouvement
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    frame_diff = cv2.absdiff(prev_gray, gray)
    thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)[1]
    motion_area = cv2.countNonZero(thresh)

    prev_gray = gray.copy()

    if motion_area > 10000:  # seuil ajustable
        # Si mouvement détecté, on passe YOLO
        results = model(frame)[0]
        person_detected = any(int(box.cls[0]) == 0 for box in results.boxes)

        if person_detected and not recording:
            video_writer, record_start_time = start_recording()
            recording = True

    if recording:
        # On réutilise les résultats YOLO précédents ou on relance si besoin
        if not person_detected:  # fallback si results n’existe pas
            results = model(frame)[0]

        # ➕ Dessiner les boxes autour des personnes
        for box in results.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            if cls_id == 0:  # personne
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                label = f"Person {conf:.2f}"
                # Dessin de la boîte
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                # Label au-dessus
                cv2.putText(frame, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # ➕ Timestamp dans la frame
        now_str = time.strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(
            frame,
            f"Timestamp: {now_str}",
            (10, frame.shape[0] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )

        # 🎥 Écriture dans la vidéo
        video_writer.write(frame)

        if time.time() - record_start_time >= RECORD_DURATION:
            print("🛑 Fin de l'enregistrement.")
            video_writer.release()
            recording = False

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Nettoyage
cap.release()
if video_writer:
    video_writer.release()
cv2.destroyAllWindows()
