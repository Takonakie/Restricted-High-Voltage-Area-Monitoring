import os
import cv2
import numpy as np
from ultralytics import YOLO
import time
import database 

if not os.path.exists("evidence"):
    os.makedirs("evidence")
    
# --- INITIAL SETUP ---
database.init_db()
print("Loading Safety Monitor Model...")
model = YOLO('yolov8n.pt')

cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)

# --- DEFINE HIGH VOLTAGE ZONE ---
danger_zone = np.array([
    [50, 50], [300, 50], 
    [300, 400], [50, 400]
], np.int32)

last_log_time = 0
COOLDOWN_SECONDS = 5

while True:
    ret, frame = cap.read()
    if not ret: break
    frame = cv2.flip(frame, 1)

    # Run Detection (CPU)
    results = model.predict(frame, conf=0.5, verbose=False, device='cpu')
    
    # Default Status
    zone_color = (0, 255, 0) # Green (Safe)
    status_text = "AREA STATUS: STERILE" 
    
    intruder_detected = False

    for box in results[0].boxes:
        class_id = int(box.cls[0])
        if class_id == 0: # Person Class
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            zone_x1, zone_y1 = 50, 50
            zone_x2, zone_y2 = 300, 400
            
            # Logika Matematika: Apakah dua kotak bertabrakan?
            # Jika (Orang Kiri < Zona Kanan) DAN (Orang Kanan > Zona Kiri) ... dst
            is_overlapping = (x1 < zone_x2) and (x2 > zone_x1) and (y1 < zone_y2) and (y2 > zone_y1)

            if is_overlapping:
                # SAMA SEPERTI SEBELUMNYA
                intruder_detected = True
                zone_color = (0, 0, 255) 
                
                # Visualisasi
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(frame, "DANGER: HIGH VOLTAGE!", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # --- DATABASE LOGGING LOGIC ---
    if intruder_detected:
        status_text = "VIOLATION: ILLEGAL ACCESS!"
        current_time = time.time()
        
        if current_time - last_log_time > COOLDOWN_SECONDS:
            # 1. Generate Nama File Unik (biar gak ketimpa)
            timestamp_str = time.strftime("%Y%m%d_%H%M%S")
            filename = f"evidence/violation_{timestamp_str}.jpg"
            
            # 2. Simpan Frame saat ini jadi Gambar (Snapshot)
            cv2.imwrite(filename, frame)
            
            # 3. Log ke Database beserta Lokasi Fotonya
            database.log_incident("CRITICAL VIOLATION: HV Zone Access", filename)
            
            last_log_time = current_time
            print(f"--- BUKTI TERSIMPAN: {filename} ---")
            
    # --- ZONE VISUALIZATION ---
    overlay = frame.copy()
    cv2.polylines(overlay, [danger_zone], isClosed=True, color=zone_color, thickness=2)
    cv2.fillPoly(overlay, [danger_zone], color=zone_color)
    frame = cv2.addWeighted(overlay, 0.3, frame, 0.7, 0)

    cv2.putText(frame, "RESTRICTED: HV PANEL", (70, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.rectangle(frame, (0,0), (640, 40), zone_color, -1) 
    cv2.putText(frame, status_text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.imshow("Industrial Safety Monitor: High Voltage", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()