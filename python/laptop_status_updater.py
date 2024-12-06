import subprocess
import json
import time
import pyrebase

# Load secrets from JSON
with open("Home_Automation\\Home-Automation\\secrets\\secrets.json", "r") as file:
    secrets = json.load(file)

# Firebase configuration
firebase_config = secrets["firebase_config"]

# Initialize Pyrebase
firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

# Firebase path and field
firebase_path_device = "Devices/Laptop1"
firebase_path_lock = "commands"
status_field_activity = "turned_on"
status_field_lock = "lock"

# Function to update Firebase status using Pyrebase
def update_status(status):
    try:
        db.child(firebase_path_device).update({status_field_activity: status})
        if status == True:
            db.child(firebase_path_lock).update({status_field_lock: False})
        print(f"Updated Firebase: {status_field_activity} -> {status}")
    except Exception as e:
        print(f"Error updating Firebase: {e}")

# Function to check if the system is locked using LogonUI process
def is_system_locked():
    try:
        process_name = "LogonUI.exe"
        output = subprocess.check_output("TASKLIST", shell=True)
        output_string = output.decode("utf-8")
        print(f"Tasklist Output:\n{output_string}")
        return process_name in output_string
    except Exception as e:
        print(f"Error checking lock status: {e}")
        return False

# Monitor system status
if __name__ == "__main__":
    try:
        update_status(True)  # Set status to true when script starts
        while True:
            locked = is_system_locked()
            update_status(not locked)  # False if locked, True otherwise
            time.sleep(0.1)  # Check every 5 seconds
    except KeyboardInterrupt:
        print("Exiting and setting status to false...")
        update_status(False)
