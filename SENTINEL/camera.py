from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")  # version légère, tu peux en prendre une plus grosse si tu veux

url = "URL"
cap = cv2.VideoCapture(url)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Effectuer la détection avec YOLO
    results = model(frame)[0]  # Une seule image à traiter
    '''
    # Pour afficher toutes les classes
    # Dessine les bounding boxes sur l'image directement
    annotated_frame = results.plot()

    # Afficher la vidéo dans une seule fenêtre
    cv2.imshow("Détection", annotated_frame)
    '''
    
    # Dessiner les bounding boxes directement sur la frame
    for box in results.boxes:
        cls = int(box.cls[0])  # Classe détectée
        if cls == 0:  # 0 = person
            # Récupérer les coordonnées de la bbox
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            # Dessiner la bounding box et le label
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, "Person", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Afficher la vidéo dans une seule fenêtre
    cv2.imshow("Détection de personnes", frame)
        
    # Quitter avec la touche 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
