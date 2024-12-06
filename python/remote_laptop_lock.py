import os
import pyrebase
import platform
import json

# Firebase configuration
with open("Home_Automation\Home-Automation\secrets\secrets.json", "r") as file:
    secrets = json.load(file)

# Access the firebase_config
firebase_config = secrets["firebase_config"]

# Initialize Firebase
firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

def lock_laptop():
    """Lock the laptop based on the OS."""
    if platform.system() == "Windows":
        os.system("rundll32.exe user32.dll, LockWorkStation")
    elif platform.system() == "Darwin":  # macOS
        os.system("osascript -e 'tell application \"System Events\" to sleep'")
    else:
        print("Lock function not supported for this OS.")

def stream_handler(message):
    """Handle database changes."""
    if message["event"] == "put" and message["path"] == "/lock":
        if message["data"] is True:
            print("Lock command received. Locking laptop...")
            lock_laptop()
        else:
            print("Lock command disabled.")

# Start the listener
print("Listening for lock commands...")
db.child("commands").stream(stream_handler)
