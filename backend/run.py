import subprocess
import time
import sys

print("==================================")
print(" STARTING AWAKE ENTERPRISE SYSTEM")
print("==================================")

# '--log-level warning' hides the noisy 200 OK messages so your terminal stays clean

backend_process = subprocess.Popen([
    sys.executable, "-m", "uvicorn", "app:app", 
    "--host", "127.0.0.1", "--port", "8000", 
    "--log-level", "warning"
])


print(" Backend Server started on http://127.0.0.1:8000")
print(" Waiting 2 seconds for server startup...\n")
time.sleep(5)

try:
    #  Launch the Vision Tracker (Pop-up will open)

    print(" Launching Camera & Vision Tracker...")
    subprocess.run([sys.executable, "vision.py"])

finally:
    #  Automatically stop the backend server when you press 'q' or close the camera

    print("\n Shutting down backend server...")
    backend_process.terminate()
    backend_process.wait()
    print(" System stopped cleanly. Goodbye!")