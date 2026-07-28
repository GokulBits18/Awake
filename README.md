#  Awake – AI Employee Posture & Fatigue Monitoring System

Awake is an AI-powered workplace monitoring system that uses computer vision to detect employee posture and fatigue in real time. It helps organizations monitor healthy sitting posture, detect drowsiness, issue instant AI voice alerts, track employee wellness and productivity, calculate performance-based bonus earnings, apply deductions for prolonged sleep, and visualize live workforce analytics through an HR dashboard.

The project combines TensorFlow Lite, MoveNet, OpenCV, FastAPI, SQLite, and a lightweight web interface to create a complete employee wellness monitoring solution.

---

##  Features

-  Employee login before starting a shift
-  Real-time webcam posture monitoring
-  AI posture classification
  - Healthy
  - Lazy
  - Sleeping
-  Eye detection for sleep verification
-  AI voice alerts when sleep is detected
-  Background API updates every second
-  Automatic productivity bonus calculation
-  Bonus deduction for prolonged sleeping
-  SQLite database for employee records
-  HR Admin Portal
-  Live dashboard updating every second
-  HR password authentication
-  One-command project launcher

---

# Project Structure

```
Awake/
│
├── app.py                 # FastAPI backend
├── vision.py              # AI vision & posture detection
├── run.py                 # Starts backend and vision system
├── frontend/
│   └── index.html         # HR Dashboard
│
├── movenet_lightning.tflite
├── awake.db
├── requirements.txt
└── README.md
```

---

# Technologies Used

## AI & Computer Vision

- TensorFlow Lite
- MoveNet Lightning
- OpenCV
- Haar Cascade Eye Detection
- NumPy

## Backend

- FastAPI
- Uvicorn
- SQLite

## Frontend

- HTML
- CSS
- JavaScript

## Voice

- Kokoro TTS
- SoundDevice

---

# How It Works

## Employee Side

1. Launch the project.
2. Enter employee name.
3. Webcam starts automatically.
4. AI analyzes:
   - Head position
   - Shoulder position
   - Eye status
5. Current posture is classified as:
   - HEALTHY
   - LAZY
   - SLEEPING
6. Every second the status is sent to the FastAPI server.
7. If sleeping continues for more than 10 seconds:
   - Voice warning is played.
   - Sleep timer increases.

---

## HR Side

The HR dashboard displays:

- Employee Name
- Current Posture
- Healthy Status
- Healthy Time
- Sleep Time
- Productivity Bonus

The table refreshes automatically every second.

---

# Productivity Scoring

## Healthy

- Earns ₹100 per hour
- Bonus accumulates every second

## Sleeping

- Sleep duration is tracked
- After one hour of accumulated sleep:
  - ₹100 is deducted
  - Sleep counter resets

---

# API Endpoints

## Admin Login

```
POST /api/admin/login
```

Request

```json
{
    "password":"admin123"
}
```

---

## Update Employee Posture

```
POST /update_posture
```

Request

```json
{
    "name":"John",
    "state":"HEALTHY"
}
```

---

## Get HR Dataset

```
GET /api/dataset
```

Returns

```json
[
  {
    "id":1,
    "name":"John",
    "current_posture":"HEALTHY",
    "is_healthy":"YES",
    "bonus_earnings":25.75,
    "healthy_time":930,
    "sleep_time":15
  }
]
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/GokulBits18/awake.git

cd awake
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---
## Dashboard password 

----- admin123  ------

## Run the Project

```bash
python run.py
```

The launcher will:

- Start the FastAPI server
- Wait for initialization
- Launch the AI vision tracker
- Shut everything down automatically when the camera closes

---

# Workflow

```
Employee
     │
     ▼
 Webcam Capture
     │
     ▼
 MoveNet Pose Detection
     │
     ▼
 Eye Detection
     │
     ▼
 AI State Classification
     │
     ▼
 FastAPI Server
     │
     ▼
 SQLite Database
     │
     ▼
 HR Dashboard
```

---

# Example States

| State | Meaning |
|--------|----------|
| HEALTHY | Proper posture |
| LAZY | Poor sitting posture |
| SLEEPING | Sleeping or eyes closed |

---

# Security

- HR password authentication
- Separate employee and HR workflows
- Local SQLite storage
- FastAPI backend with CORS support

---

# Future Improvements

- Face recognition login
- Employee attendance tracking
- Email notifications
- Weekly productivity reports
- AI analytics dashboard
- PostgreSQL/MySQL support
- Docker deployment
- Cloud synchronization
- Mobile dashboard
- Multi-camera support

---

# Author

**Gokul **

AI Engineer | Computer Vision | Machine Learning | Deep Learning | FastAPI

GitHub:
https://github.com/GokulBits18

---

## pic

<img width="1192" height="580" alt="image" src="https://github.com/user-attachments/assets/d98f8be2-b8d7-4727-bdf5-e8c074ce0dd2" />

<img width="816" height="501" alt="image" src="https://github.com/user-attachments/assets/67bdcdd0-9a33-48d8-9db0-c0f9ab4741d7" />


