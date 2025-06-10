import math
import osascript
import time

class Hand:
    THUMB_TIP = 4
    INDEX_TIP = 8

    VOLUME_MIN = 0
    VOLUME_MAX = 100
    MIN_DISTANCE = 0.02
    MAX_DISTANCE = 0.35

    OPEN_HAND_THRESHOLD = 0.2
    ACTION_COOLDOWN = 2.0

    def __init__(self):
        self.previous_position = None
        self.last_action_time = 0
        self.is_playing = True

    def can_perform_action(self) -> bool:
        return time.time() - self.last_action_time >= self.ACTION_COOLDOWN

    def calculate_distance_landmarks(self, landmark1, landmark2) -> float:
        return math.sqrt(
            (landmark1.x - landmark2.x)**2 + 
            (landmark1.y - landmark2.y)**2 + 
            (landmark1.z - landmark2.z)**2
        )

    def detect_movement(self, hand_landmarks) -> str:
        if not self.can_perform_action():
            return None

        thumb = hand_landmarks.landmark[self.THUMB_TIP]
        index = hand_landmarks.landmark[self.INDEX_TIP]
        
        distance = self.calculate_distance_landmarks(thumb, index)
        
        if distance > self.OPEN_HAND_THRESHOLD:
            self.last_action_time = time.time()
            self.is_playing = not self.is_playing
            return "pause" if self.is_playing else "play"
            
        direction = "next" if thumb.x < index.x else "previous"
        self.last_action_time = time.time()
        return direction

    def set_volume(self, volume: float) -> None:
        try:
            volume = max(self.VOLUME_MIN, min(self.VOLUME_MAX, int(volume * 100)))
            osascript.osascript(f"set volume output volume {volume}")
        except Exception as e:
            print(f"Error setting volume: {e}")

    def detect_pinch(self, hand_landmarks) -> None:
        distance = self.calculate_distance_landmarks(
            hand_landmarks.landmark[self.THUMB_TIP],
            hand_landmarks.landmark[self.INDEX_TIP]
        )
        
        normalized_distance = max(0, min(1, 
            (distance - self.MIN_DISTANCE) / (self.MAX_DISTANCE - self.MIN_DISTANCE)
        ))
        
        volume = normalized_distance
        self.set_volume(volume)

    def reset(self) -> None:
        self.previous_position = None
        self.is_playing = True