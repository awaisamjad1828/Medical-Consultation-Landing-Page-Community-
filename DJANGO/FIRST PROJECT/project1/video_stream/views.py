import cv2
import numpy as np
from django.http import StreamingHttpResponse
import os
import winsound  # For sound alert on Windows

# Path to model files
base_dir = os.path.dirname(os.path.abspath(__file__))
prototxt_path = os.path.join(base_dir, "static", "models", "MobileNetSSD_deploy.prototxt")
caffemodel_path = os.path.join(base_dir, "static", "models", "MobileNetSSD_deploy.caffemodel")

# Load the model
person_net = cv2.dnn.readNetFromCaffe(prototxt_path, caffemodel_path)

# Class labels for MobileNet SSD
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant",
           "sheep", "sofa", "train", "tvmonitor"]

# Generalized function to generate frames
def generate_frames(video_source):
    cap = cv2.VideoCapture(video_source)  # Camera source (0 for system camera, IP for external)
    heatmap = np.zeros((480, 640), dtype=np.float32)  # Adjust size as per video resolution
    heatmap_decay = 0.95  # Decay factor for the heatmap

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)

        # Perform detection
        person_net.setInput(blob)
        detections = person_net.forward()

        person_count = 0  # Initialize person count

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            if confidence > 0.5:  # Confidence threshold
                idx = int(detections[0, 0, i, 1])

                if CLASSES[idx] == "person":
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")

                    person_count += 1  # Count detected persons

                    # Draw bounding box and label on the frame
                    cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                    label = f"Person {confidence * 100:.2f}%"
                    cv2.putText(frame, label, (startX, startY - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    # Update heatmap for detected person region
                    heatmap[startY:endY, startX:endX] += 1

        # Apply decay to the heatmap
        heatmap *= heatmap_decay

        # Normalize the heatmap for visualization
        normalized_heatmap = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)
        heatmap_colored = cv2.applyColorMap(normalized_heatmap.astype(np.uint8), cv2.COLORMAP_JET)

        # Resize heatmap to match the frame size
        heatmap_colored_resized = cv2.resize(heatmap_colored, (frame.shape[1], frame.shape[0]))

        # Overlay the heatmap on the original frame
        overlay = cv2.addWeighted(frame, 0.7, heatmap_colored_resized, 0.3, 0)

        # If more than 3 people are detected, play an alert sound
        if person_count > 3:
            winsound.Beep(1000, 500)  # Frequency 1000 Hz, duration 500ms

        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', overlay)
        frame = buffer.tobytes()

        # Yield frame for streaming
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    cap.release()

# Functions for video feeds
def video_feed(request):
    return StreamingHttpResponse(generate_frames(0),  # System camera
                                 content_type='multipart/x-mixed-replace; boundary=frame')

def video_feed_ip(request):
    return StreamingHttpResponse(generate_frames('http://192.168.1.6:8080/video'),  # IP camera
                                 content_type='multipart/x-mixed-replace; boundary=frame')

def home(request):
    return render(request, 'video_stream/home.html')

import cv2
import os
import time
import uuid
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render

# Global variables for video capture
recording = False
cap = None
out = None

def video_recording(request):
    global recording, cap, out

    if request.method == 'POST':  # Handle AJAX POST requests
        action = request.POST.get('action')

        if action == 'start':
            if not recording:
                # Start recording
                recording = True
                cap = cv2.VideoCapture(0)  # Open the camera
                fourcc = cv2.VideoWriter_fourcc(*'XVID')

                # Generate a unique filename using the current timestamp or UUID
                unique_filename = f"recording_{int(time.time())}.avi"  # Timestamp-based filename
                output_dir = os.path.join('media', 'recordings')  # Save directory
                os.makedirs(output_dir, exist_ok=True)

                file_name = os.path.join(output_dir, unique_filename)
                out = cv2.VideoWriter(file_name, fourcc, 20.0, (640, 480))

                return JsonResponse({'status': f'Recording started. Saving to {file_name}'})

        elif action == 'stop':
            if recording:
                # Stop recording
                recording = False
                if cap:
                    cap.release()
                if out:
                    out.release()
                cv2.destroyAllWindows()

                # Provide the saved file path in the response
                saved_file_path = out.filename if out else "Unknown"
                return JsonResponse({'status': f'Recording stopped and saved to {saved_file_path}'})

        return JsonResponse({'status': 'Invalid action.'})

    return render(request, 'video_recording.html')


# Stream video to the client
def video_feed(request):
    global cap
    if cap is None:
        cap = cv2.VideoCapture(0)  # Open the camera if not already open

    def generate():
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            ret, jpeg = cv2.imencode('.jpg', frame)
            if ret:
                frame = jpeg.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return StreamingHttpResponse(generate(), content_type='multipart/x-mixed-replace; boundary=frame')
