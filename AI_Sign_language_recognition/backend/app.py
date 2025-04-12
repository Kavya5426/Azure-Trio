from flask import Flask, Response, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import tensorflow as tf
import os

app = Flask(__name__)
CORS(app)

# Load trained model
MODEL_PATH = "model/sign_language_model.h5"
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
model = tf.keras.models.load_model(MODEL_PATH)

# Class labels
CLASS_LABEL_PATH = "model/class_labels.txt"
with open(CLASS_LABEL_PATH, "r") as f:
    CLASS_LABELS = [line.strip() for line in f]

# Globals
video_stream = None
streaming = False



# Frame pre-processing
def preprocess_frame(frame):
    img = cv2.resize(frame, (64, 64))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img


# Video stream class
class VideoStream:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.running = self.cap.isOpened()

    def get_frame(self):
        global current_prediction
        ret, frame = self.cap.read()
        if not ret:
            return None



# Route to start video
@app.route('/start_video')
def start_video():
    global video_stream, streaming
    if not streaming:
        video_stream = VideoStream()
        streaming = True
        print(" Video stream started.")
        return jsonify({"status": "started"})
    return jsonify({"status": "already running"})


# Route to stream video
@app.route('/video_feed')
def video_feed():
    global video_stream, streaming

    if video_stream is None or not video_stream.running:
        return "Camera not started", 400

    def generate():
        global video_stream, streaming
        while streaming and video_stream and video_stream.running:
            frame = video_stream.get_frame()
            if frame is None:
                break
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        if video_stream:
            video_stream.release()

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')






# Home route
@app.route('/')
def index():
    return "Real-time Sign Language Prediction Server Running. Use /start_video to begin."


# Run server
if __name__ == '__main__':
    print("Running at http://127.0.0.1:5000")
    app.run(debug=True)




