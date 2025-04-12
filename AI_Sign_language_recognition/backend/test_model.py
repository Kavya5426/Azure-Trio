import tensorflow as tf

MODEL_PATH = "model/sign_language_model.h5"

try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print("Model loaded successfully!")
    model.summary()  # Prints model architecture
except Exception as e:
    print(f"Error loading model: {e}")
