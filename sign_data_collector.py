import cv2
import os
import time
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.7,
                       min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

label = input("Enter label name for the sign: ").strip()
save_dir = os.path.join("dataset", label)

if not os.path.exists(save_dir):
    os.makedirs(save_dir)
    print(f"Directory created for label: {save_dir}")
else:
    print(f"Directory already exists: {save_dir}")

cap = cv2.VideoCapture(0)
count = 0
max_images = 100

print("Starting in 3 seconds. Get ready...")
time.sleep(3)
print("Recording started. Press 'q' to quit.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    image = cv2.flip(frame, 1)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_image)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmarks = []
            for lm in hand_landmarks.landmark:
                landmarks.append([lm.x, lm.y, lm.z])

            if count < max_images:
                filename = os.path.join(save_dir, f"{label}_{count}.txt")
                with open(filename, "w") as f:
                    for l in landmarks:
                        f.write(','.join(map(str, l)) + '\n')
                count += 1
                cv2.putText(image, f"Recording {count}/{max_images}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(image, "Data Collection Complete", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Sign Data Collector", image)
    if cv2.waitKey(1) & 0xFF == ord('q') or count >= max_images:
        break

cap.release()
cv2.destroyAllWindows()