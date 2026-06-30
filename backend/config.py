import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_DIR = os.path.join(BASE_DIR, "models")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "outputs")
TEMP_FOLDER = os.path.join(BASE_DIR, "temp")

CHILLER_MODEL_PATH = os.path.join(MODEL_DIR, "Only_Chiller.pt")
GENERAL_MODEL_PATH = os.path.join(MODEL_DIR, "shelf.pt")
NESTLE_MODEL_PATH = os.path.join(MODEL_DIR, "best.onnx")

CONFIDENCE_THRESHOLD = 0.50
IOU_THRESHOLD = 0.30

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(TEMP_FOLDER, exist_ok=True)