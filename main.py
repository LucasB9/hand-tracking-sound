import cv2
import mediapipe as mp
import osascript
from contextlib import contextmanager
from handleHand import Hand

CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720
VOLUME_MIN = 0
VOLUME_MAX = 100
THUMB_TIP = 4
INDEX_TIP = 8

MUSIC_COMMANDS = {
    'play': 'tell application "Spotify" to play',
    'pause': 'tell application "Spotify" to pause',
    'next': 'tell application "Spotify" to next track',
    'previous': 'tell application "Spotify" to previous track',
}

@contextmanager
def camera_capture():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
    try:
        yield cap
    finally:
        cap.release()
        cv2.destroyAllWindows()

def control_music(command):
    try:
        if command in MUSIC_COMMANDS:
            osascript.osascript(MUSIC_COMMANDS[command])
        else:
            print(f"Unknown command: {command}")
    except Exception as e:
        print(f"Error controlling Spotify: {e}")

def main():
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands
    volume_hand = Hand()
    music_hand = Hand()
    
    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5
    ) as hands, camera_capture() as cap:
        while True:
            success, frame = cap.read()
            if not success:
                print("Failed to capture frame")
                break

            RGB_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(RGB_frame)

            if results.multi_hand_landmarks:
                for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                    mp_drawing.draw_landmarks(
                        frame, 
                        hand_landmarks, 
                        mp_hands.HAND_CONNECTIONS
                    )
                    
                    is_left_hand = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x < 0.5
                    
                    if is_left_hand:
                        volume_hand.detect_pinch(hand_landmarks)
                    else:
                        movement = music_hand.detect_movement(hand_landmarks)
                        if movement:
                            print("movement", movement)
                            if movement == "next":
                                control_music('next')
                            elif movement == "previous":
                                control_music('previous')
                            elif movement == "play":
                                control_music('play')
                            elif movement == "pause":
                                control_music('pause')

            cv2.imshow("Hand Tracking", frame)
            
            key = cv2.waitKey(1)
            if key == ord('q'):
                break

if __name__ == "__main__":
    main()
