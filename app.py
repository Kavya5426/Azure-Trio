from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import signal
import os

app = Flask(__name__)
CORS(app)  # Enable CORS so React can talk to Flask

# Global variable to store the subprocess
process = None

@app.route("/")
def home():
    return "Flask is running..."

@app.route("/start_prediction", methods=["POST"])
def start_prediction():
    global process
    if process is None:
        try:
            # Start the predict_sign.py script
            process = subprocess.Popen(["python", "predict_sign.py"])
            return jsonify({"status": "started"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"message": "Prediction already running."})

@app.route("/stop_prediction", methods=["POST"])
def stop_prediction():
    global process
    if process:
        try:
            os.kill(process.pid, signal.SIGTERM)
            process = None
            return jsonify({"status": "stopped"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"message": "No prediction process to stop."})

if __name__ == "__main__":
    print("Flask server is starting...")
    app.run(debug=True)
