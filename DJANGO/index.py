import cv2
import numpy as np
import winsound  # For sound alert on Windows

# Load pre-trained model for person detection (MobileNet SSD with Caffe model)
net = cv2.dnn.readNetFromCaffe(
    "deploy.prototxt", "res10_300x300_ssd_iter_140000.caffemodel"
)

# Initialize video capture
cap = cv2.VideoCapture(0)  # Change to video file path if using a video

# Create a blank heatmap
heatmap = np.zeros((480, 640), dtype=np.float32)  # Adjust size as per video resolution
heatmap_decay = 0.95  # Decay factor for the heatmap

while True:
    ret, frame = cap.read()
    if not ret:
        break

    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))

    # Perform detection
    net.setInput(blob)
    detections = net.forward()

    person_count = 0

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        if confidence > 0.5:  # Confidence threshold
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            label = "Person"
            person_count += 1

            # Draw bounding box and label
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
            cv2.putText(frame, label, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Update heatmap for detected person region
            heatmap[startY:endY, startX:endX] += 1

    # Apply decay to the heatmap
    heatmap *= heatmap_decay

    # Normalize the heatmap for visualization
    normalized_heatmap = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)
    heatmap_colored = cv2.applyColorMap(normalized_heatmap.astype(np.uint8), cv2.COLORMAP_JET)

    # Overlay the heatmap on the original frame
    overlay = cv2.addWeighted(frame, 0.7, heatmap_colored, 0.3, 0)

    # Display person count on the frame
    cv2.putText(overlay, f"Person Count: {person_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Check if the area is crowded
    if person_count > 3:
        cv2.putText(overlay, "Crowded Area!", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 3)
        winsound.Beep(1000, 500)  # Alert sound (frequency 1000 Hz, duration 500 ms)

    # Show video frame with heatmap overlay
    cv2.imshow("Person Detection with Heatmap", overlay)

    # Break loop on 'q' key press
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:  # 'q' or 'Esc' key to exit
        break

# Release video capture and close windows
cap.release()
cv2.destroyAllWindows()
