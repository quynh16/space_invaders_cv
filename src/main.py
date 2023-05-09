import mediapipe as mp
import cv2
from models import *
import threading
import queue


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


def detect_hand(hand_detector, input_queue, output_queue, stop_event):
    while not stop_event.is_set():
        try:
            # get a frame from the input queue
            frame = input_queue.get(timeout=1)

            # detect hand gestures in the frame
            frame, results = hand_detector.detect(frame)

            # put the updated frame and results into the output queue
            output_queue.put((frame, results))

        except queue.Empty:
            pass

    # clear the input queue to release any blocked put calls
    input_queue = None


def main():
    camera = Camera()
    hand_detector = HandDetector()
    game = Game()

    # create stop event flag
    # stop_event = threading.Event()

    # # create input and output queues
    # input_queue = queue.Queue()
    # output_queue = queue.Queue()

    # # create a thread for hand detection
    # detection_thread = threading.Thread(target=detect_hand, args=(hand_detector, input_queue, output_queue, stop_event))
    # detection_thread.start()


    while True:
        # # get frames from camera
        # frame = camera.read()

        # # Draw the hand landmarks on the frame
        # # Convert the BGR image to RGB before processing
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # # put the frame into the input queue
        # input_queue.put(frame)

        # # check if there's an updated frame and results in the output queue
        # if not output_queue.empty():
        #     frame, results = output_queue.get()

        #     frame.flags.writeable = True
        #     frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        #     # update the game state given hand detection results
        #     # frame = game.update(frame, results)

        # cv2.imshow('Hand Space Invaders', frame)

        # # Exit events
        # if cv2.waitKey(1) == ord('q') or not camera.is_visible('Hand Space Invaders'):
        #     # set the stop event flag to stop the detection_thread
        #     stop_event.set()
        #     break

        # get frames from camera
        frame = camera.read()

        # Draw the hand landmarks on the frame
        # Convert the BGR image to RGB before processing
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # detect hand from given frame and draw landmarks on it
        frame, results = hand_detector.detect(frame)

        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)     

        # update the game state given hand detection results
        frame = game.update(frame, results)

        cv2.imshow('Hand Hockey Game', frame)

        # Exit events
        if cv2.waitKey(1) == ord('q') or not camera.is_visible('Hand Hockey Game'):
            break

    camera.release()
    cv2.destroyAllWindows()
    # wait for the detection_thread to finish
    # detection_thread.join()


if __name__ == '__main__':
    main()
