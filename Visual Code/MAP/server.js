const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const ffmpeg = require('fluent-ffmpeg');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

// Path to the camera's RTSP stream (replace with your camera's URL)
const cameraUrl = 'rtsp://<http://192.168.1.10:4747/video/stream';

// Serve the index.html file
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

// Stream the video
io.on('connection', (socket) => {
    console.log('Client connected');
    
    // Using FFmpeg to stream video from IP camera
    const stream = ffmpeg(cameraUrl)
        .inputOptions('-rtsp_transport tcp') // Use TCP for RTSP to avoid packet loss
        .outputFormat('mjpeg') // Output format for MJPEG streaming
        .videoCodec('mjpeg')  // MJPEG codec for live streaming
        .noAudio()
        .on('start', () => {
            console.log('FFmpeg started streaming');
        })
        .on('error', (err) => {
            console.log('FFmpeg error: ' + err.message);
        })
        .on('end', () => {
            console.log('FFmpeg streaming ended');
        });

    // Pipe FFmpeg output to the client via socket.io
    stream.pipe(socket);
});

// Start the server
server.listen(3000, () => {
    console.log('Server is running on http://localhost:3000');
});

