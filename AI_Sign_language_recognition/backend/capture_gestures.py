import cv2
import os
import time

# Settings
gesture_name = "No"  # 🔁 Change to 'Yes', 'No', 'Please' as needed
save_video_dir = f"videos/{gesture_name}"
save_frame_dir = f"dataset/{gesture_name}"
video_duration = 3  # seconds
frame_rate = 20

# Create folders if they don't exist
os.makedirs(save_video_dir, exist_ok=True)
os.makedirs(save_frame_dir, exist_ok=True)

cap = cv2.VideoCapture(0)
print("Webcam is on. Press 'c' to capture...")

recording = False
video_path = ""

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Webcam - Press 'c' to capture", frame)

    key = cv2.waitKey(1)

    # Press 'c' to capture video
    if key == ord('c') and not recording:
        recording = True
        print("Recording started...")
        video_path = os.path.join(save_video_dir, f"{gesture_name}_{int(time.time())}.avi")

        # Define video writer
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(video_path, fourcc, frame_rate, (frame.shape[1], frame.shape[0]))

        start_time = time.time()
        while time.time() - start_time < video_duration:
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)
            cv2.imshow("Recording...", frame)

        out.release()
        print("Recording complete.")
        recording = False

        # Now extract frames
        print("Extracting frames...")
        cap_vid = cv2.VideoCapture(video_path)
        count = 0
        while True:
            ret, frame = cap_vid.read()
            if not ret:
                break
            frame_path = os.path.join(save_frame_dir, f"{gesture_name}_{count}.jpg")
            cv2.imwrite(frame_path, frame)
            count += 1

        cap_vid.release()
        print(f"Saved {count} frames to {save_frame_dir}")

    # Press 'q' to quit
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
