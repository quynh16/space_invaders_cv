import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


def main():
    camera = cv2.VideoCapture(0)

    with mp_hands.Hands(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:
        while True:
            ret, frame = camera.read()

            if not ret:
                print("Failed to capture video.")
                break

            # Flip the image horizontally for a later selfie-view display
            frame = cv2.flip(frame, 1)

            # Convert the BGR image to RGB before processing
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # To improve performance, optionally mark the image as not writeable to pass by reference.
            frame.flags.writeable = False
            results = hands.process(frame)

            # Draw the hand landmarks on the frame
            frame.flags.writeable = True
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS)

            # Use the landmarks to detect hand gestures
            # Add your code here to detect hand gestures using the landmarks in results

            cv2.imshow('Camera', frame)

            # exit events
            if cv2.waitKey(1) == ord('q'):
                break
            if cv2.getWindowProperty('Camera', cv2.WND_PROP_VISIBLE) < 1:
                break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
