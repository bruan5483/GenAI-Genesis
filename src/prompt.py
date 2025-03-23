import os
import vertexai
from vertexai.preview.generative_models import GenerativeModel

# Set Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/bryant.ruan/Desktop/GenAI Genesis/utils/google_service_token.json"

# Initialize Vertex AI with your project
PROJECT_ID = "genai-genesis-454502"
vertexai.init(project=PROJECT_ID, location="us-central1")

# Load the Gemini model
text_model = GenerativeModel("gemini-pro")

def remove_special_characters(s):
    s = s.replace("#", "")
    s = s.replace("*", "")
    return s

def generate_text(prompt):
    """Generates a response from Gemini Pro given a prompt."""
    params = {
        "temperature": 0.2,
        "max_output_tokens": 1024
    }
    try:
        p = "Do NOT include any special characters in the response (for example, no # or *). You are a travel guide leading a tourist around. Given this image description: " + prompt + ", identify if this scene contains a famous landmark or site. Provide a concise and understandable landmark description for the tourist in flowing sentences. If there is no landmark, only return \"No landmark found\" and NOTHING ELSE. Do NOT EVER ask questions to get additional details."
        resp = text_model.generate_content(p, generation_config=params)
        return remove_special_characters(resp.text)
    except Exception as e:
        return f"Error generating text: {e}"
