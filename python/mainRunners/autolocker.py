import subprocess

# Start both scripts
process1 = subprocess.Popen(["python", "Home_Automation\Home-Automation\python\\remote_laptop_lock.py"])
process2 = subprocess.Popen(["python", "Home_Automation\Home-Automation\python\laptop_status_updater.py"])

try:
    # Keep the main script running as long as the subprocesses are active
    process1.wait()
    process2.wait()
except KeyboardInterrupt:
    print("Terminating processes...")
    process1.terminate()
    process2.terminate()
