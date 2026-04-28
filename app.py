from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import subprocess
import os
import uuid

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "separated"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/extract", methods=["POST"])
def extract_vocals():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400

    file = request.files["audio"]
    unique_id = str(uuid.uuid4())
    input_path = os.path.join(UPLOAD_FOLDER, f"{unique_id}_{file.filename}")

    file.save(input_path)

    try:
        subprocess.run([
            "demucs",
            "--two-stems=vocals",
            input_path
        ], check=True)

        filename = os.path.splitext(os.path.basename(input_path))[0]
        vocal_path = os.path.join(
            "separated",
            "htdemucs",
            filename,
            "vocals.wav"
        )

        return send_file(vocal_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)