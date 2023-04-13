import cv2
import mediapipe as mp


def main():
    camera = cv2.VideoCapture(0)
    while True:
        ret, frame = camera.read()

        if not ret:
            print("Failed to capture video.")
            break

        cv2.imshow('Camera', frame)

        if cv2.waitKey(1) == ord('q'):
            break
        if cv2.getWindowProperty('Camera', cv2.WND_PROP_VISIBLE) < 1:
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
