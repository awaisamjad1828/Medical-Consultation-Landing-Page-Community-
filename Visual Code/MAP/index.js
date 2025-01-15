// index.js
const express = require("express");
const cors = require("cors");
const ffmpeg = require("fluent-ffmpeg");

const app = express();
const port = 5000;

app.use(cors()); // Enable CORS for all origins

// Replace with your IP camera RTSP stream URL
const cameraStreamUrl = "rtsp://your_camera_ip/stream";

// Stream the camera feed to the frontend as MJPEG
app.get("/video_feed", (req, res) => {
  res.contentType("multipart/x-mixed-replace; boundary=frame");

  // Use ffmpeg to read the RTSP stream and convert it to MJPEG
  ffmpeg(cameraStreamUrl)
    .inputOptions("-rtsp_transport tcp") // Option for RTSP stream over TCP
    .outputFormat("mjpeg")
    .videoCodec("mjpeg")
    .noAudio()
    .on("start", () => {
      console.log("Streaming started...");
    })
    .on("error", (err) => {
      console.log("Error in stream:", err);
      res.status(500).send("Error streaming footage");
    })
    .on("end", () => {
      console.log("Streaming ended...");
    })
    .pipe(res, { end: true }); // Pipe the video stream to the response
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
