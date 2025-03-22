import os
import time
import tempfile
import threading
from google.cloud import texttospeech
from playsound import playsound

# Import the detection module to access the latest object
import objectDetection

# Set credentials (update the path if needed)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/bryant.ruan/Desktop/GenAI Genesis/utils/power-workhorse-key.json"

# Initialize Google Cloud Text-to-Speech client
tts_client = texttospeech.TextToSpeechClient()

def tts_loop():
    last_spoken = None  # Track last spoken object to avoid repeats

    # Configure voice settings
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
    )
    
    while True:
        current_obj = objectDetection.get_focused_object()
        if current_obj and current_obj.name != last_spoken:
            synthesis_input = texttospeech.SynthesisInput(text=current_obj.name)
            response = tts_client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            # Write the audio content to a temporary MP3 file and play it
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as out:
                out.write(response.audio_content)
                tmp_filename = out.name
            playsound(tmp_filename)
            os.remove(tmp_filename)
            last_spoken = current_obj.name
        
        time.sleep(1)  # Check for updates every second

def start_tts_loop():
    """Starts the TTS loop in a background thread."""
    thread = threading.Thread(target=tts_loop, daemon=True)
    thread.start()
    return thread
