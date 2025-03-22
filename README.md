# GenAI-Genesis

## Description
A Hackathon Project

## Installation
For this project, you will need:
- Raspberry Pi (Raspbian)
- ArduCam Module for Raspberry Pi
- Micro-HDMI to HDMI Cable

#### Clone repository
```
git clone https://github.com/bruan5483/GenAI-Genesis.git
cd GenAI-Genesis
```

#### Create Python venv
```
python -m venv ./venv
source ./venv/bin/activate
```

#### Dependencies
```
pip install numpy
pip install opencv-python-headless
pip install google-cloud-vision
pip install google-cloud-texttospeech
pip install google-cloud-aiplatform
pip install playsound==1.2.2
```

#### Google Cloud API Key
Follow Google Cloud setup here: https://developers.google.com/workspace/guides/get-started
Download the API_KEY and put it in ```./utils/google_service_token.json```

## Usage

## License
The MIT Licence applies to this project. Refer to LICENSE.md