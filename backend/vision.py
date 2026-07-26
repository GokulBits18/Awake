import cv2
import tensorflow as tf
import numpy as np
import time
import requests
import threading
import sounddevice as sd
from kokoro import KPipeline
import tkinter as tk
from tkinter import simpledialog

#  GUI POP-UP FOR NAME 
root = tk.Tk()
root.withdraw() # Hides the main blank Tkinter window
EMPLOYEE_NAME = simpledialog.askstring("Awake Employee System", "Enter your name to start your shift:")

# If the user clicks 'Cancel' or closes the box

if not EMPLOYEE_NAME:
    print("Shift cancelled. Exiting...")
    exit()

EMPLOYEE_NAME = EMPLOYEE_NAME.strip()
print(f"\nWelcome, {EMPLOYEE_NAME}! Starting tracking...\n")



MODEL_PATH = "movenet_lightning.tflite"
interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
cap = cv2.VideoCapture(0)

# Sleep tracking 

sleep_start_time = None
SLEEP_THRESHOLD_SECONDS = 10 
last_update_time = time.time()

# Kokoro Voice Engine

print(" Loading Voice Engine...")
pipeline = KPipeline(lang_code='a') 
is_speaking = False

def play_warning(text):
    global is_speaking
    if is_speaking:
        return
    is_speaking = True
    def speak_thread():
        global is_speaking
        try:
            generator = pipeline(text, voice='af_heart', speed=1.0)
            for _, _, audio in generator:
                sd.play(audio, samplerate=24000)
                sd.wait()
        except Exception as e:
            print(f" Voice error: {e}")
        finally:
            is_speaking = False
    threading.Thread(target=speak_thread, daemon=True).start()


def send_posture_async(name, state):
    try:
        payload = {"name": name, "state": state}
        
        requests.post("https://awake-enterprise.onrender.com/update_posture", json=payload, timeout=5.0)
    except Exception as e:
        print(f"Connection Error: {e}")


while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
        
    img = frame.copy()
    img = tf.image.resize_with_pad(np.expand_dims(img, axis=0), 192, 192)
    input_image = tf.cast(img, dtype=tf.float32)
    
    interpreter.set_tensor(input_details[0]['index'], input_image.numpy())
    interpreter.invoke()
    keypoints_with_scores = interpreter.get_tensor(output_details[0]['index'])
    keypoints = keypoints_with_scores[0][0]
    height, width, _ = frame.shape
    
    nose = keypoints[0]
    left_shoulder = keypoints[5]
    right_shoulder = keypoints[6]
    
    upper_body_visible = (nose[2] > 0.3 and left_shoulder[2] > 0.3 and right_shoulder[2] > 0.3)
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    open_eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    eyes_are_open = len(open_eyes) > 0
    
    if upper_body_visible:
        avg_shoulder_y = (left_shoulder[0] + right_shoulder[0]) / 2.0
        nose_y = nose[0]
        vertical_dist = avg_shoulder_y - nose_y
        
        if vertical_dist < 0.06 or not eyes_are_open:
            candidate_state = "SLEEPING"
        elif vertical_dist < 0.11:
            candidate_state = "LAZY"
        else:
            candidate_state = "HEALTHY"
            
        current_time = time.time()
        
        if candidate_state == "SLEEPING":
            if sleep_start_time is None: sleep_start_time = current_time
            elapsed_sleep = current_time - sleep_start_time
            
            if elapsed_sleep >= SLEEP_THRESHOLD_SECONDS:
                state = "SLEEPING"
                color = (0, 0, 255) 
                play_warning(f"Wake up, {EMPLOYEE_NAME}! Get back to work!")
            else:
                state = f"SLEEPING DETECTED ({int(SLEEP_THRESHOLD_SECONDS - elapsed_sleep)}s)"
                color = (0, 165, 255) 
        else:
            sleep_start_time = None  
            state = candidate_state
            color = (0, 255, 0) if state == "HEALTHY" else (0, 165, 255)

        
        if current_time - last_update_time >= 1.0:
            clean_state = state.split()[0]
            
            threading.Thread(target=send_posture_async, args=(EMPLOYEE_NAME, clean_state), daemon=True).start()
            last_update_time = current_time

        cv2.putText(frame, f"State: {state}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        cv2.putText(frame, f"Dist: {vertical_dist:.2f} | Eyes Open: {eyes_are_open}", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    # Draw Skeleton
    EDGES = [(0, 1), (0, 2), (1, 3), (2, 4), (5, 6), (5, 7), (7, 9), (6, 8), (8, 10), (5, 11), (6, 12), (11, 12)]
    for edge in EDGES:
        p1, p2 = edge
        y1, x1, score1 = keypoints[p1]
        y2, x2, score2 = keypoints[p2]
        if score1 > 0.3 and score2 > 0.3:
            cv2.line(frame, (int(x1 * width), int(y1 * height)), (int(x2 * width), int(y2 * height)), (0, 0, 255), 2)

    for kp in keypoints:
        y, x, score = kp
        if score > 0.3: 
            cv2.circle(frame, (int(x * width), int(y * height)), 5, (255, 255, 255), -1)

    cv2.imshow(f'Awake Terminal - {EMPLOYEE_NAME}', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()
