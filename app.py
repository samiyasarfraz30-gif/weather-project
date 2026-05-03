from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import numpy as np
import json

from model_loader import load_model
from utils import process_image, serial_processing, parallel_processing

app = Flask(__name__)
CORS(app)  # ✅ yeh add karo

# Fix all paths relative to this file's location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "../uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load model once
model = load_model()

# Load labels — fixed path
with open(os.path.join(BASE_DIR, "labels.json")) as f:
    labels = json.load(f)


# -------------------------
# HOME ROUTE
# -------------------------
@app.route("/")
def home():
    return "Weather Prediction API Running"


# -------------------------
# PREDICTION ROUTE
# -------------------------
@app.route("/predict", methods=["POST"])
def predict():
    try:
        print("Prediction request received")

        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # ---------------- SERIAL ----------------
        serial_imgs, serial_time = serial_processing([file_path])

        # ---------------- PARALLEL ----------------
        parallel_imgs, parallel_time = parallel_processing([file_path])

        # safety check
        if len(serial_imgs) == 0:
            return jsonify({"error": "Image processing failed"}), 500

        img = np.array(serial_imgs[0]).reshape(1, 224, 224, 3)

        prediction = model.predict(img)
        predicted_class = str(np.argmax(prediction))

        result = {
            "prediction": labels[predicted_class],
            "serial_time": float(serial_time),
            "parallel_time": float(parallel_time)
        }

        print("Response:", result)
        return jsonify(result)

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)