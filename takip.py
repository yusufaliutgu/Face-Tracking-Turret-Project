import cv2
from cvzone.FaceDetectionModule import FaceDetector
import serial
import time

# ==========================================
# CONFIGURATION & PARAMETERS
# ==========================================
SERIAL_PORT = 'COM5'      # Communication port
BAUD_RATE = 9600          # Serial communication speed
CAMERA_ID = 0             # Default webcam index

# --- Calibration Settings ---
# Axis Inversion (Set True if movement is reversed)
INVERT_X_AXIS = True
INVERT_Y_AXIS = True

# Mechanical Offsets (Fine-tuning for laser alignment)
OFFSET_X = -5
OFFSET_Y = 25

# Motion Smoothing (0.1 - 0.3 recommended for stability)
SMOOTHING_FACTOR = 0.15

# ==========================================
# SYSTEM INITIALIZATION
# ==========================================

# Initialize Serial Connection
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # Wait for Arduino reset
    print(f"[INFO] Serial connection established on {SERIAL_PORT}")
except Exception as e:
    print(f"[ERROR] Serial connection failed: {e}")
    exit()

# Initialize Computer Vision
cap = cv2.VideoCapture(CAMERA_ID)
detector = FaceDetector(minDetectionCon=0.5)

# Current servo positions (initialized to center)
current_x = 90.0
current_y = 90.0

# ==========================================
# MAIN LOOP
# ==========================================
while True:
    success, img = cap.read()
    if not success:
        print("[WARNING] Failed to read from camera.")
        continue

    # Face Detection
    img, bboxs = detector.findFaces(img, draw=False)

    if bboxs:
        # Get the first face detected
        center = bboxs[0]["center"]
        x, y, w, h = bboxs[0]["bbox"]
        
        # Draw Visuals
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.circle(img, center, 5, (0, 0, 255), cv2.FILLED)

        # Map Screen Coordinates to Servo Degrees (0-180)
        target_x = int((center[0] / 640) * 180)
        target_y = int((center[1] / 480) * 180)

        # Apply Axis Inversion
        if INVERT_X_AXIS: target_x = 180 - target_x
        if INVERT_Y_AXIS: target_y = 180 - target_y

        # Apply Smoothing (Software Damper)
        current_x = current_x + (target_x - current_x) * SMOOTHING_FACTOR
        current_y = current_y + (target_y - current_y) * SMOOTHING_FACTOR

        # Apply Calibration Offsets
        final_x = int(current_x) + OFFSET_X
        final_y = int(current_y) + OFFSET_Y

        # Constrain Values (Safety Limit: 0-180)
        final_x = max(0, min(180, final_x))
        final_y = max(0, min(180, final_y))

        # Send Data to Microcontroller
        data_packet = f"{final_x},{final_y}\n"
        try:
            ser.write(data_packet.encode())
        except Exception as e:
            pass # Ignore momentary serial write errors

    # Display Output
    cv2.imshow("Turret System Vision", img)

    # Exit Condition (Press 'q')
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()