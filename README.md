# Awake - Enterprise Vision System

Awake is an AI-powered, real-time posture and alertness tracking system designed for enterprise network environments. It monitors employee ergonomics and wakefulness using advanced computer vision, routing analytics to a secure, centralized HR dashboard.

## Features

* **Real-Time Skeleton Tracking:** Uses TensorFlow Lite and MoveNet to map upper body keypoints (shoulders, nose) and draw a visual skeleton overlay.
* **Alertness Detection:** Combines spatial distance calculations with OpenCV Haar Cascades to detect drooping posture and closed eyes.
* **Personalized Voice Alerts:** Integrates Kokoro TTS in a non-blocking background thread to verbally warn employees (e.g., "Wake up, [Name]! Get back to work!") if they fall asleep.
* **Enterprise Architecture:** Separates the client (camera tracker) from the server (database and HR portal). Handles concurrent data streams from multiple employees simultaneously.
* **Dynamic Bonus Calculation:** Automatically calculates financial bonuses based on seconds spent in a "Healthy" posture, and applies penalties for prolonged sleeping.
* **Secure HR Dashboard:** A real-time web portal protected by a master admin password to view live company-wide analytics.

## Tech Stack

* **Machine Learning / Computer Vision:** TensorFlow Lite (MoveNet), OpenCV (`haarcascade_eye.xml`)
* **Backend:** FastAPI, Python `requests`, SQLite3
* **Frontend:** HTML5, CSS3, Vanilla JavaScript, Tkinter (for GUI pop-ups)
* **Audio:** Kokoro Voice Engine, Sounddevice
* **Concurrency:** Python `threading`, `subprocess`, `BackgroundTasks` (FastAPI)

##  Project Structure

```text
Awake/
│
├── backend/
│   ├── app.py                  # Main FastAPI server and SQLite database logic
│   ├── vision.py               # Employee client script (Camera, ML models, TTS)
│   ├── run.py                  # Optional all-in-one launcher script
│   ├── index.html              # Secure HR Admin portal
│   └── movenet_lightning.tflite # Pre-trained ML model

##Installation & Setup
**Clone the repository and navigate to the project directory:

**Bash
cd Awake/backend

##Create and activate a virtual environment (recommended):

**Bash
python -m venv pos
pos\Scripts\activate  # Windows
# source pos/bin/activate # Mac/Linux

**Install the required dependencies:
**(Ensure you have PyTorch, TensorFlow, OpenCV, FastAPI, Uvicorn, and Kokoro installed in your environment).

##How to Run (Local Testing)
You can run the system using two separate terminals for the cleanest output.

Terminal 1: Start the Admin Server

##Bash
uvicorn app:app 
Open your web browser and navigate to http://127.0.0.1:8000/index.html. Log in with the master password (admin123).

Terminal 2: Start the Employee Client

##Bash
python vision.py
A prompt will ask for your name. Once entered, the camera will activate and begin streaming your posture data to the server.



