import cv2
from my_utils.colors import *


class Table:
    def __init__(self, outer_padding=1, inner_padding=25, circle_radius=100, 
                 color=RED_RGB, thickness=2):
        self.color = color
        self.thickness = thickness
        self.outer_padding = outer_padding
        self.inner_padding = inner_padding
        self.circle_radius = circle_radius
        
        self.initialized = False
        self.center = None
        self.w = None
        self.h = None
        self.l1 = None
        self.l2 = None
        self.g1 = None
        self.g2 = None
        self.g3 = None
        self.g4 = None

    def draw(self, frame):
        if not self.initialized:
            self.h, self.w = frame.shape[:2]
            self.center = (int(self.w/2), int(self.h/2))
            self.l1 = (int(self.w/2), 0)
            self.l2 = (int(self.w/2), self.h)
            self.g1 = (0, int(self.h/3))
            self.g2 = (self.inner_padding + 1, int(2*self.h/3))
            self.g3 = (self.w - self.inner_padding - 1, int(self.h/3))
            self.g4 = (self.w, int(2*self.h/3))
            self.initialized = True

        # outer rectangle
        frame = cv2.rectangle(frame, (self.outer_padding, self.outer_padding), 
                              (self.w - self.outer_padding, self.h - self.outer_padding), 
                              self.color, self.thickness)  
        # inner rectangle
        frame = cv2.rectangle(frame, (self.inner_padding, self.inner_padding), 
                              (self.w - self.inner_padding, self.h-self.inner_padding), self.color, 
                              self.thickness)
        # center circle
        frame = cv2.circle(frame, self.center, self.circle_radius, self.color, self.thickness)  
        # center line
        frame = cv2.line(frame, self.l1, self.l2, self.color, self.thickness)
        # left goal
        frame = cv2.rectangle(frame, self.g1, self.g2, self.color, -1) 
        # right goal
        frame = cv2.rectangle(frame, self.g3, self.g4, self.color, -1) 
        return frame
