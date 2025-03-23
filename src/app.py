from flask import Flask, render_template, request, redirect, url_for
import subprocess
import os
import signal
import multiprocessing
import cv2
import threading

app = Flask(__name__)

# Store process references
process = None

# Function to run the script asynchronously
def run_process(mode):
    global process
    if mode == "main":
        process = subprocess.Popen(["python", "src/main.py"], preexec_fn=os.setsid)
    elif mode == "translate":
        process = subprocess.Popen("python src/translate.py", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Capture output asynchronously
        def capture_output():
            stdout, stderr = process.communicate()
            print(f"STDOUT: {stdout.decode()}")
            print(f"STDERR: {stderr.decode()}")
        
        # Run output capture in a separate thread
        threading.Thread(target=capture_output).start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run():
    global process
    mode = request.form.get('mode')

    # Stop any running process safely
    if process is not None:
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            print(f"Terminated previous process {process.pid}")
        except ProcessLookupError:
            print("Process was not found, skipping termination.")
        process = None

    # Start the selected mode asynchronously
    threading.Thread(target=run_process, args=(mode,)).start()

    return redirect(url_for('index'))

@app.route('/stop', methods=['POST'])
def stop():
    global process
    if process is not None:
        try:
            pid = process.pid
            if pid:  # Check if process has a valid PID
                os.killpg(os.getpgid(pid), signal.SIGTERM)
                print(f"Process {pid} terminated.")
        except ProcessLookupError:
            print("Process already stopped or not found.")
        except AttributeError:
            print("Process object is None, skipping termination.")
        finally:
            process = None  # Reset the process variable

        # Explicit cleanup
        try:
            cv2.destroyAllWindows()  # Close any OpenCV windows
            cv2.VideoCapture(0).release()  # Release the camera if it was used
        except Exception as e:
            print(f"Error during cleanup: {e}")

        # Explicitly clean up resources from multiprocessing
        try:
            for child in multiprocessing.active_children():
                print(f"Terminating child process {child.pid}")
                child.terminate()
        except Exception as e:
            print(f"Error cleaning up multiprocessing resources: {e}")

        return "Script stopped."
    return "No active process to stop."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
