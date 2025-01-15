const axios = require('axios');
const fs = require('fs');
const path = require('path');
const ffmpeg = require('fluent-ffmpeg');

// IP Camera URL (replace with your actual camera IP)
const cameraUrl = 'http://192.168.1.10:4747/video';
const outputDirectory = './'; // Directory where video files will be saved
const videoDuration = 10 * 60; // 10 minutes in seconds
const retryInterval = 5 * 60 * 1000; // 5 minutes in milliseconds

let recording = false;

// Function to start recording from the MJPEG stream
const startRecording = () => {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-'); // Format timestamp for filename
  const outputFile = path.join(outputDirectory, `video-${timestamp}.mp4`);

  // Start recording the stream
  const stream = ffmpeg(cameraUrl)
    .inputFormat('mjpeg')
    .output(outputFile)
    .duration(videoDuration)
    .on('start', () => {
      console.log(`Recording started: ${outputFile}`);
      recording = true;
    })
    .on('end', () => {
      console.log(`Recording saved: ${outputFile}`);
      recording = false;
      startRecording(); // Start the next recording automatically after current one finishes
    })
    .on('error', (err) => {
      console.error('Error while recording:', err);
      recording = false;
      setTimeout(startRecording, retryInterval); // Retry after 5 minutes if there was an error
    })
    .run();
};

// Function to continuously record until there's an error
const startContinuousRecording = () => {
  if (!recording) {
    startRecording();
  } else {
    console.log('Already recording. Waiting...');
  }
};

// Start the recording process
startContinuousRecording();
