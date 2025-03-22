import vertexai
from vertexai.preview.vision_models import Image, ImageTextModel
import os
import objectDetection
import time
import threading
import cv2
import tempfile

# Shared variable for latest caption
_latest_caption = "No caption available."
_caption_lock = threading.Lock()

# Set credentials (update the path as needed)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/bryant.ruan/Desktop/GenAI Genesis/utils/google_service_token.json"

PROJECT_ID = "genai-genesis-454502"
vertexai.init(project=PROJECT_ID, location="us-central1")

model = ImageTextModel.from_pretrained("imagetext@001")

def get_latest_caption():
    """Returns the most recent caption."""
    with _caption_lock:
        return _latest_caption

def gemini_loop():
    global _latest_caption
    
    while True:
        frame = objectDetection.get_latest_frame()
        if frame is None:
            time.sleep(1)
            continue

        # Convert frame to JPG and write to a temporary file
        success, encoded_image = cv2.imencode('.jpg', frame)
        if not success:
            time.sleep(1)
            continue

        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file.write(encoded_image.tobytes())
            temp_filename = temp_file.name

        # Load the image from the temporary file
        source_img = Image.load_from_file(temp_filename)

        # **Use VQA to get a detailed description**
        vqa_response = model.ask_question(
            image=source_img,
            question="Describe the main object in frame in detail.",
        )

        description_text = vqa_response.text if vqa_response else "No description generated."

        # Store the description in a shared variable
        with _caption_lock:
            _latest_caption = description_text

        print(f"[Gemini] Description: {description_text}")

        # Remove the temporary file
        try:
            os.remove(temp_filename)
        except Exception as e:
            print(f"[Gemini] Warning: Failed to delete temp file - {e}")

        time.sleep(10)  # Increase delay between requests

def start_gemini_loop():
    """Starts the Gemini loop in a background thread."""
    #print("[Gemini] Starting Gemini processing thread...")
    thread = threading.Thread(target=gemini_loop, daemon=True)
    thread.start()
    return thread
