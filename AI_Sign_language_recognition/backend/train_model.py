import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Test if it works
datagen = ImageDataGenerator(rescale=1./255)
print("ImageDataGenerator imported successfully!")

# Paths
DATASET_DIR = 'dataset'  # Subfolders: Hello/, Ok/, Yes/, Please/, No/, etc.
MODEL_SAVE_PATH = 'model/sign_language_model.h5'
LABELS_SAVE_PATH = 'model/class_labels.txt'

# Image settings
IMAGE_SIZE = (64, 64)
BATCH_SIZE = 32
EPOCHS = 15  # Slightly increased for better learning

# Create ImageDataGenerator with validation split
datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

# Load training and validation data
train_generator = datagen.flow_from_directory(
    DATASET_DIR,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training',
    shuffle=True
)

val_generator = datagen.flow_from_directory(
    DATASET_DIR,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation'
)

# Automatically detect class labels
class_labels = list(train_generator.class_indices.keys())
print(f"Detected Classes: {class_labels}")

# Save class labels
os.makedirs(os.path.dirname(LABELS_SAVE_PATH), exist_ok=True)
with open(LABELS_SAVE_PATH, 'w') as f:
    for label in class_labels:
        f.write(label + '\n')

# Define CNN model
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(64, 64, 3)),
    tf.keras.layers.MaxPooling2D(2,2),
    
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),

    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),

    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(len(class_labels), activation='softmax')  # Dynamic class count
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train model
history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=EPOCHS
)

# Save the trained model
model.save(MODEL_SAVE_PATH)
print(f"Model saved to {MODEL_SAVE_PATH}")



