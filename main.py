import cv2
import mediapipe as mp
import osascript
import math
from contextlib import contextmanager

CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720
VOLUME_MIN = 0
VOLUME_MAX = 100
THUMB_TIP = 4
INDEX_TIP = 8

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

def calculate_distance_landmarks(landmark1, landmark2):
    return math.sqrt(
        (landmark1.x - landmark2.x)**2 + 
        (landmark1.y - landmark2.y)**2 + 
        (landmark1.z - landmark2.z)**2
    )

def set_volume(volume):
    try:
        volume = max(VOLUME_MIN, min(VOLUME_MAX, int(volume * 100)))
        osascript.osascript(f"set volume output volume {volume}")
    except Exception as e:
        print(f"Error setting volume: {e}")

def main():
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands
    
    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
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
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        frame, 
                        hand_landmarks, 
                        mp_hands.HAND_CONNECTIONS
                    )
                    
                    distance = calculate_distance_landmarks(
                        hand_landmarks.landmark[THUMB_TIP],
                        hand_landmarks.landmark[INDEX_TIP]
                    )
                    set_volume(distance)

            cv2.imshow("Hand Tracking", frame)
            
            key = cv2.waitKey(1)
            if key == ord('q'):  
                break

if __name__ == "__main__":
    main()
