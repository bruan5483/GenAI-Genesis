import vertexai
from vertexai.preview.vision_models import Image, ImageTextModel
import os

# Set credentials (update the path as needed)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/bryant.ruan/Desktop/GenAI Genesis/utils/google_service_token.json"    

# TODO(developer): Update and un-comment below lines
PROJECT_ID = "genai-genesis-454502"
input_file = "/Users/bryant.ruan/Desktop/GenAI Genesis/utils/images/input-image3.jpg"

vertexai.init(project=PROJECT_ID, location="us-central1")

model = ImageTextModel.from_pretrained("imagetext@001")
source_img = Image.load_from_file(location=input_file)

captions = model.get_captions(
    image=source_img,
    # Optional parameters
    language="en",
    number_of_results=1,
)

print(captions)