import cv2
import os
import datetime
import threading
import sounddevice as sd
import soundfile as sf
from moviepy.editor import *
# Create a directory to save videos if it doesn't exist
output_dir = "recorded_videos"
os.makedirs(output_dir, exist_ok=True)

recording = False
audio_filename = None
video_filename = None

def record_audio():
    global audio_filename, recording
    audio_filename = os.path.join(output_dir, f"audio_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.wav")
    with sf.SoundFile(audio_filename, mode='x', samplerate=44100, channels=2, subtype='PCM_16') as file:
        print("Audio recording started.")
        while recording:
            audio_data = sd.rec(int(44100 * 0.1), samplerate=44100, channels=2, dtype='int16')
            sd.wait()
            file.write(audio_data)
    print("Audio recording stopped.")

def record_video():
    global video_filename, recording
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Unable to access the camera.")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    codec = cv2.VideoWriter_fourcc(*'XVID')
    video_filename = os.path.join(output_dir, f"video_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.avi")
    out = cv2.VideoWriter(video_filename, codec, 20.0, (frame_width, frame_height))

    print("Video recording started.")
    while recording:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)
        cv2.imshow("Recording Video - Press 'q' to stop", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("Video recording stopped.")

def start_recording():
    global recording
    if recording:
        print("Recording is already in progress.")
        return

    recording = True
    threading.Thread(target=record_audio, daemon=True).start()
    threading.Thread(target=record_video, daemon=True).start()

def stop_recording():
    global recording
    if not recording:
        print("No recording in progress.")
        return

    recording = False
    print("Stopping recording...")

    # Wait for threads to complete
    threading.Event().wait(1)

    # Synchronize video and audio
    if video_filename and audio_filename:
        combine_audio_video(video_filename, audio_filename)

def combine_audio_video(video_path, audio_path):
    output_file = os.path.join(output_dir, f"output_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4")
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)
    video_with_audio = video_clip.set_audio(audio_clip)
    video_with_audio.write_videofile(output_file, codec="libx264")
    print(f"Video with audio saved as {output_file}")

def main():
    import tkinter as tk
    root = tk.Tk()
    root.title("Video Recorder with Audio")

    tk.Button(root, text="Start Recording", command=start_recording, bg="green", fg="white", width=20).pack(pady=10)
    tk.Button(root, text="Stop Recording", command=stop_recording, bg="red", fg="white", width=20).pack(pady=10)
    tk.Label(root, text="Press 'q' in the video window to stop recording.").pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
