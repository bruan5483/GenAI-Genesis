import os
import time
import tempfile
import threading
from google.cloud import texttospeech
from playsound import playsound
import objectDetection
import gemini

# Set credentials (update the path if needed)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/bryant.ruan/Desktop/GenAI Genesis/utils/google_service_token.json"

# Initialize Google Cloud Text-to-Speech client
tts_client = texttospeech.TextToSpeechClient()

def tts_loop():
    #print("[TTS] Starting text-to-speech loop...")
    last_spoken = None  # Track last spoken caption to avoid repeats

    # Configure voice settings
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    while True:
        # Get the latest caption from Gemini
        current_caption = gemini.get_latest_caption()
        
        if current_caption and current_caption != last_spoken:
            #print(f"[TTS] Speaking: {current_caption}")
            synthesis_input = texttospeech.SynthesisInput(text=current_caption)
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
            last_spoken = current_caption  # Avoid repeating the same caption
        
        time.sleep(2)  # Check for new captions every 2 seconds

def start_tts_loop():
    """Starts the TTS loop in a background thread."""
    #print("[TTS] Starting TTS thread...")
    thread = threading.Thread(target=tts_loop, daemon=True)
    thread.start()
    return thread
