import cv2
import os

def extract_frames(video_path, out_dir="C:/Users/Sathwik/myprojects/frames", frame_interval=10):
    # Create output directory if it doesn't exist
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Cannot open video file at {video_path}")
        return 0

    count = 0       # Total frames read
    frame_id = 0    # Saved frame count

    while True:
        success, frame = cap.read()
        if not success:
            break  # Exit loop when no more frames

        if count % frame_interval == 0:
            filename = os.path.join(out_dir, f"frame_{frame_id}.jpg")
            cv2.imwrite(filename, frame)
            frame_id += 1

        count += 1

    cap.release()
    return frame_id
