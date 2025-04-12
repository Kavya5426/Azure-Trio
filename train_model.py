import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
import joblib

data_dir = "dataset"
X = []
y = []

for label in os.listdir(data_dir):
    label_path = os.path.join(data_dir, label)
    for file in os.listdir(label_path):
        file_path = os.path.join(label_path, file)
        with open(file_path, 'r') as f:
            lines = f.readlines()
            landmarks = [float(num) for line in lines for num in line.strip().split(',')]
            X.append(landmarks)
            y.append(label)

X = np.array(X)
y = np.array(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=500)
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)
print(f"Model accuracy: {accuracy * 100:.2f}%")

joblib.dump(model, "sign_model.pkl")