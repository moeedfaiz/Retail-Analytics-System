import os
import uuid
from pathlib import Path

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

from config import UPLOAD_FOLDER, OUTPUT_FOLDER
from detector import process_image

app = Flask(__name__)
CORS(app)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "success": True,
        "message": "Retail Analytics API is running.",
        "endpoints": {
            "analyze": "/analyze",
            "outputs": "/outputs/<filename>"
        }
    })


@app.route("/analyze", methods=["POST"])
def analyze():
    if "image" not in request.files:
        return jsonify({
            "success": False,
            "message": "No image uploaded. Use form-data key: image"
        }), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({
            "success": False,
            "message": "Empty filename."
        }), 400

    original_name = secure_filename(file.filename)
    ext = Path(original_name).suffix.lower()

    if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
        ext = ".jpg"

    upload_filename = f"upload_{uuid.uuid4().hex}{ext}"
    upload_path = os.path.join(UPLOAD_FOLDER, upload_filename)

    file.save(upload_path)

    try:
        result = process_image(upload_path)

        output_filename = result["output_image"]

        result["output_image"] = (
            request.host_url.rstrip("/") + "/outputs/" + output_filename
        )

        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


@app.route("/outputs/<path:filename>", methods=["GET"])
def serve_output(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        use_reloader=False
    )