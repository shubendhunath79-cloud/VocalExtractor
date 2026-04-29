from flask import Flask, request, send_file
from flask_cors import CORS
import os
import subprocess

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "Vocal Extractor API is running"

@app.route("/extract", methods=["POST"])
def extract():
    if "audio" not in request.files:
        return "No file uploaded", 400

    file = request.files["audio"]
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)

    output_path = os.path.join(OUTPUT_FOLDER, "vocals.wav")

    # Demucs command (runs separation)
    try:
        subprocess.run([
            "python", "-m", "demucs",
            "-o", OUTPUT_FOLDER,
            input_path
        ], check=True)

        # Find output vocals (Demucs output structure)
        base_name = os.path.splitext(file.filename)[0]
        vocal_path = os.path.join(
            OUTPUT_FOLDER,
            "htdemucs",
            base_name,
            "vocals.wav"
        )

        return send_file(vocal_path, as_attachment=True)

    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)