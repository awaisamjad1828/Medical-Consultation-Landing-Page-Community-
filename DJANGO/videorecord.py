import cv2
import os
import datetime

# Create a directory to save videos if it doesn't exist
output_dir = "recorded_videos"
os.makedirs(output_dir, exist_ok=True)

def record_video():
    # Open the default camera (usually 0 for the primary camera)
    cap = cv2.VideoCapture("http://192.168.1.7:8080/video")
    if not cap.isOpened():
        print("Error: Unable to access the camera.")
        return

    # Get the video frame width and height
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define the codec and create a VideoWriter object
    codec = cv2.VideoWriter_fourcc(*'XVID')  # Codec for .avi files
    video_filename = os.path.join(output_dir, f"video_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.avi")
    out = cv2.VideoWriter(video_filename, codec, 20.0, (frame_width, frame_height))

    print(f"Recording started. Video will be saved as {video_filename}")
    print("Press 'q' to stop recording.")

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            print("Error: Unable to fetch frame from camera.")
            break

        # Write the frame to the video file
        out.write(frame)

        # Show the frame
        cv2.imshow("Recording - Press 'q' to stop", frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Stopping recording...")
            break

    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("Recording stopped and resources released.")

if __name__ == "__main__":
    record_video()
