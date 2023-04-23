import numpy as np
import cv2
from my_utils.colors import *
import numpy as np

class Game:
    def __init__(self, color=BLUE_RGB, scale=3, thickness=0.02):
        self.initialized = False
        self.w = None
        self.h = None
        self.pos = 0.5 # percentage of width
        self.len = 0.1
        self.color = color
        self.thickness = thickness

        # scale up hand position so it doesn't need to move entire width of screen
        self.scale = scale 

    def update(self, frame, results):
        if not self.initialized:
            self.h, self.w = frame.shape[:2]
            self.initialized = True

        self.move(results)
        return self.draw(frame)
    
    def draw(self, frame):
        frame = cv2.rectangle(frame, (int(self.w * (self.pos - self.len / 2)), 
                                      int(self.h * (1 - self.thickness))), 
                                     (int(self.w * (self.pos + self.len / 2)), 
                                      int(self.h)), 
                                          self.color, thickness=-1)  
        return frame

    def move(self, results):
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                hand_x = hand_landmarks.landmark[8].x
                thumb = hand_landmarks.landmark[4].x
                
                thumb_thresh = hand_landmarks.landmark[4].x
                if thumb > thumb_thresh:
                    self.shoot()

                self.pos = (hand_x - 0.5) * self.scale + 0.5

                if self.pos > 1 - self.len:
                    self.pos = 1 - self.len / 2
                if self.pos < 0 + self.len:
                    self.pos = self.len / 2

    def shoot(self):
        print("PEW!")
        