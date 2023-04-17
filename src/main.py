import mediapipe as mp
import cv2
from models import *


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


def calculate_hand_position(hand_landmarks, image_width, image_height):
    # Get the landmarks for the wrist and middle finger tip
    wrist_landmark = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
    middle_finger_tip_landmark = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

    # Calculate the position of the hand as the center of the wrist and middle finger tip
    hand_position_x = int((wrist_landmark.x + middle_finger_tip_landmark.x) * 0.5 * image_width)
    hand_position_y = int((wrist_landmark.y + middle_finger_tip_landmark.y) * 0.5 * image_height)

    return (hand_position_x, hand_position_y)


def main():
    camera = Camera()
    hand_detector = HandDetector()
    table = Table()

    while True:
        frame = camera.read()

        frame = hand_detector.detect(frame)
        frame = table.draw(frame)

        cv2.imshow('Hand Hockey Game', frame)

        # Exit events
        if cv2.waitKey(1) == ord('q') or not camera.is_visible('Hand Hockey Game'):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
