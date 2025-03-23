import cv2
import os
import time
import io
from google.cloud import vision
from google.cloud import translate_v2 as translate
from google.cloud import texttospeech
import pygame
from PIL import Image

# Set credentials (update the path if needed)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/bryant.ruan/Desktop/GenAI Genesis/utils/google_service_token.json"

# Set up Google Cloud API clients
vision_client = vision.ImageAnnotatorClient()
translate_client = translate.Client()
tts_client = texttospeech.TextToSpeechClient()

# Initialize pygame mixer for audio playback
pygame.mixer.init()

def extract_text_from_image(frame):
    """Converts an OpenCV frame to bytes and extracts text using Google Cloud Vision API."""
    success, encoded_image = cv2.imencode('.jpg', frame)
    if not success:
        return ""

    image_bytes = encoded_image.tobytes()
    image = vision.Image(content=image_bytes)
    
    response = vision_client.text_detection(image=image)
    texts = response.text_annotations

    return texts[0].description if texts else ""

def translate_text(text, target_language="en"):
    """Translates text to English using Google Cloud Translation API."""
    if not text.strip():
        return ""
    
    result = translate_client.translate(text, target_language=target_language)
    return result.get("translatedText", "")

def text_to_speech(text):
    """Converts text to speech using Google Cloud Text-to-Speech API and plays it."""
    if not text.strip():
        return
    
    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",  # Change if needed
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = tts_client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Define the audio directory and filename
    audio_dir = "utils/audio"
    os.makedirs(audio_dir, exist_ok=True)  # Ensure the directory exists
    audio_file = os.path.join(audio_dir, "output.mp3")

    # Save the audio file
    with open(audio_file, "wb") as out:
        out.write(response.audio_content)

    # Play the audio
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

    # Wait until audio playback finishes
    while pygame.mixer.music.get_busy():
        time.sleep(1)

def capture_and_translate():
    """Captures camera feed, extracts text, translates, and speaks."""
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Extract text using Google Cloud Vision API
        detected_text = extract_text_from_image(frame)
        print("Detected Text:", detected_text)

        if detected_text:
            # Translate to English
            translated_text = translate_text(detected_text)
            print("Translated Text:", translated_text)

            # Convert to speech
            text_to_speech(translated_text)

        # Display the camera feed
        cv2.imshow("Camera Feed", frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_and_translate()
