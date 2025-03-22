import cv2
import time
import threading
import os
import numpy as np
from google.cloud import vision

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/bryant.ruan/Desktop/GenAI Genesis/utils/genai-genesis-454502-bd2726684d79.json"    

# Initialize Google Cloud Vision client
client = vision.ImageAnnotatorClient()

# Open webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Reduce resolution for faster processing
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Shared frame & lock
frame = None
lock = threading.Lock()
focused_object = None  # Store the highest-confidence object

# Function to process frames asynchronously
def process_frame():
    global frame, focused_object
    while True:
        with lock:
            if frame is None:
                continue
            img = frame.copy()
        
        # Convert frame to bytes
        _, encoded_image = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 50])  # Compress image
        image_bytes = encoded_image.tobytes()
        
        # Send to Google Cloud Vision
        image = vision.Image(content=image_bytes)
        response = client.object_localization(image=image)
        
        # Find the most confident object
        highest_confidence = 0
        best_object = None
        
        for obj in response.localized_object_annotations:
            if obj.score > highest_confidence:  # Prioritize the most confident object
                highest_confidence = obj.score
                best_object = obj
        
        # Store only the best object
        with lock:
            focused_object = best_object
        
        time.sleep(0.5)  # Process frames at a slower rate to avoid excessive API calls

# Start background thread
thread = threading.Thread(target=process_frame, daemon=True)
thread.start()

# Main loop
while cap.isOpened():
    start_time = time.time()
    
    ret, frame = cap.read()
    if not ret:
        break

    # Update shared frame for processing thread
    with lock:
        frame = cv2.resize(frame, (640, 480))  # Reduce image size

    # Draw bounding box for the focused object
    if focused_object:
        name = focused_object.name
        vertices = [(int(v.x * frame.shape[1]), int(v.y * frame.shape[0])) for v in focused_object.bounding_poly.normalized_vertices]
        
        if len(vertices) == 4:
            cv2.rectangle(frame, vertices[0], vertices[2], (0, 255, 0), 2)
            cv2.putText(frame, name, (vertices[0][0], vertices[0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Display frame
    fps = 1.0 / (time.time() - start_time)
    cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow('Focused Object Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
