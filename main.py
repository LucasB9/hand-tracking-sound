import cv2
import mediapipe as mp
import osascript

print(cv2.__version__)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
    
while True:
    success, frame = cap.read()
    if success:
        RGB_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(RGB_frame)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        cv2.imshow("Hand Tracking", frame)
        key = cv2.waitKey(1)
        if key == ord('a'):
            print("a")
            osascript.osascript("set volume output volume 30")
        if key == ord('d'):
            print("d")
            osascript.osascript("set volume output volume 100")
        if key == ord('q'):
            break
