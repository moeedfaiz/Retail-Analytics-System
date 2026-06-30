from ultralytics import YOLO
from config import *

print("===================================")
print("Loading AI Models...")
print("===================================")

# Chiller Detection Model
chiller_model = YOLO(CHILLER_MODEL_PATH)

# General SKU Detection Model
general_model = YOLO(GENERAL_MODEL_PATH)

# Nestlé Detection Model
nestle_model = YOLO(NESTLE_MODEL_PATH)

print("✅ Chiller Model Loaded")
print("✅ General SKU Model Loaded")
print("✅ Nestlé Model Loaded")
print("===================================")