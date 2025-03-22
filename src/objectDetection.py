import cv2
import time
import threading
import os
import numpy as np
from google.cloud import vision

# Set credentials (update the path as needed)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/bryant.ruan/Desktop/GenAI Genesis/utils/google_service_token.json"    

# Initialize Google Cloud Vision client
client = vision.ImageAnnotatorClient()

# Shared variables and lock for thread-safe access
_latest_frame = None
_focused_object = None
_lock = threading.Lock()

def detection_loop():
    global _latest_frame, _focused_object
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Faster processing resolution
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    while cap.isOpened():
        ret, frame_read = cap.read()
        if not ret:
            break
        
        # Resize frame and update shared variable
        frame_resized = cv2.resize(frame_read, (640, 480))
        with _lock:
            _latest_frame = frame_resized.copy()
        
        # Convert frame to JPEG bytes for the API call
        _, encoded_image = cv2.imencode('.jpg', frame_resized, [cv2.IMWRITE_JPEG_QUALITY, 50])
        image_bytes = encoded_image.tobytes()
        image = vision.Image(content=image_bytes)
        
        # Call the Vision API for object localization
        response = client.object_localization(image=image)
        
        # Select the object with the highest confidence score
        highest_confidence = 0
        best_object = None
        for obj in response.localized_object_annotations:
            if obj.score > highest_confidence:
                highest_confidence = obj.score
                best_object = obj
        
        with _lock:
            _focused_object = best_object
        
        time.sleep(0.5)  # Slow down API calls
    
    cap.release()

def start_detection():
    """Starts the detection loop in a background thread."""
    thread = threading.Thread(target=detection_loop, daemon=True)
    thread.start()
    return thread

def get_focused_object():
    """Returns the most recently detected object (or None)."""
    with _lock:
        return _focused_object

def get_latest_frame():
    """Returns the most recent frame (or None if not available)."""
    with _lock:
        return _latest_frame.copy() if _latest_frame is not None else None
