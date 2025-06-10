# Hand Gesture Music Control

A Python application that allows you to control your music playback using hand gestures captured through your webcam. The application uses MediaPipe for hand tracking and AppleScript to control Spotify.

## Features

- **Volume Control**: Adjust volume by pinching your thumb and index finger

  - Close pinch = Lower volume
  - Wide pinch = Higher volume

- **Music Control**:
  - Open hand = Toggle play/pause
  - Thumb left of index = Previous track
  - Thumb right of index = Next track

## Requirements

- Python 3.7+
- macOS (for Spotify control)
- Webcam
- Spotify installed

## Dependencies

```bash
pip install mediapipe opencv-python osascript
```

## Usage

1. Run the application:

```bash
python main.py
```

2. Position your hands in front of the camera:

   - Right hand: Control volume using pinch gesture
   - Left hand: Control music playback using gestures

3. Keyboard shortcuts:
   - 'q': Quit application

## Gesture Guide

### Volume Control (Right Hand)

- Pinch your thumb and index finger together to lower volume
- Spread them apart to increase volume

### Music Control (Left Hand)

- Open your hand to toggle play/pause
- Point your thumb to the left of your index finger for previous track
- Point your thumb to the right of your index finger for next track

## Technical Details

- Uses MediaPipe for hand tracking
- Implements gesture recognition for precise control
- Controls Spotify through AppleScript
- Real-time hand tracking visualization

## Notes

- Make sure you have good lighting for accurate hand tracking
- Keep your hands within the camera frame
- Wait for the cooldown period (2 seconds) between actions
- The application works best with a clear view of your hands
