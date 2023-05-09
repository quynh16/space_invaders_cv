import cv2
import mediapipe as mp


class HandDetector:
    def __init__(self, min_detection_confidence=0.7, min_tracking_confidence=0.7):
        self.hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence)
        self.drawing_utils = mp.solutions.drawing_utils

    def detect(self, frame):
        # Convert the BGR image to RGB before processing
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # To improve performance, optionally mark the image as not writeable to pass by reference.
        frame.flags.writeable = False

        # Process the frame to detect hand landmarks
        results = self.hands.process(frame)

        # Draw the hand landmarks on the frame
        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.drawing_utils.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp.solutions.hands.HAND_CONNECTIONS)
                
        return frame, results