import cv2
from my_utils.colors import *


class Table:
    def __init__(self, color = YELLOW_RGB, thickness=2):
        self.color = color
        self.thickness = thickness

    def draw(self, frame):
        frame = cv2.rectangle(frame, (50, 30), (950, 470), self.color, self.thickness)  # outer border
        frame = cv2.rectangle(frame, (80, 50), (920, 450), self.color, self.thickness)  # inner border
        frame = cv2.circle(frame, (500, 250), 50, self.color, self.thickness)  # center circle
        frame = cv2.line(frame, (500, 30), (500, 470), self.color, self.thickness)  # center line
        return frame
