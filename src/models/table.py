import cv2
from my_utils.colors import *


class Table:
    def __init__(self, width=900, height=550, color=YELLOW_RGB, thickness=2):
        self.width = width
        self.height = height
        self.color = color
        self.thickness = thickness
        self.r1 = (50, 30)
        self.r2 = (50 + self.width, 30 + self.height)
        self.r3 = (50 + 25, 30 + 25)
        self.r4 = (50 + self.width - 25, 30 + self.height - 25)
        self.c = (50 + int(self.width/2), 30 + int(self.height/2))
        self.l1 = (50 + int(self.width/2), 30)
        self.l2 = (50 + int(self.width/2), 30+self.height)
        self.g1 = (50, 30 + int(self.height/3))
        self.g2 = (100, 30 + int(2*self.height/3))
        self.g3 = (50 + self.width-50, 30 + int(self.height/3))
        self.g4 = (50+self.width, 30 + int(2*self.height/3))

    def draw(self, frame):
        frame = cv2.rectangle(frame, self.r1, self.r2, self.color, self.thickness)  # outer border
        frame = cv2.rectangle(frame, self.r3, self.r4, self.color, self.thickness)  # inner border
        frame = cv2.circle(frame, self.c, 50, self.color, self.thickness)  # center circle
        frame = cv2.line(frame, self.l1, self.l2, self.color, self.thickness)  # center line
        frame = cv2.rectangle(frame, self.g1, self.g2, RED_RGB, -1)
        frame = cv2.rectangle(frame, self.g3, self.g4, RED_RGB, -1)
        return frame
