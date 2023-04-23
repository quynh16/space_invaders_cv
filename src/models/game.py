import numpy as np
import cv2
from my_utils.colors import *
import numpy as np
import random

class Game:
    def __init__(self, color=BLUE_RGB, scale=3, thickness=0.02):
        self.initialized = False
        self.w = None
        self.h = None
        self.pos = 0.5 # percentage of width
        self.thumb = None
        self.len = 0.1 # length of rectangel
        self.color = color
        self.thickness = thickness
        self.trigger = False

        # scale up hand position so it doesn't need to move entire width of screen
        self.scale = scale 
        
        self.bullets = []

    def update(self, frame, results):
        if not self.initialized:
            self.h, self.w = frame.shape[:2]
            self.initialized = True

        self.move(results)

        return self.draw(frame)
    
    def draw_bullets(self, frame):
        for bullet in self.bullets:
            x, y = bullet.pos()
            if y < 0:
                self.bullets.remove(bullet) # remove bullet if off screen

            # draw bullet
            frame = cv2.rectangle(frame, (int(x * self.w), int(y * self.h)), 
                                 (int((x+0.01) * self.w), int((y+0.05) * self.h)), 
                                  self.color, thickness=-1) 

            bullet.update() # update bullet position 
        
        return frame

    def draw(self, frame):
        frame = cv2.rectangle(frame, (int(self.w * (self.pos - self.len / 2)), 
                                      int(self.h * (1 - self.thickness))), 
                                     (int(self.w * (self.pos + self.len / 2)), 
                                      int(self.h)), 
                                          self.color, thickness=-1)  
        frame = self.draw_bullets(frame)
        return frame

    def move(self, results):
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                hand_x = hand_landmarks.landmark[8].x
                self.thumb = hand_landmarks.landmark[4].x

                self.thumb_thresh = hand_landmarks.landmark[5].x
                if self.thumb > self.thumb_thresh:
                    self.trigger = True
                
                if self.trigger and self.thumb < self.thumb_thresh:
                    self.shoot()
                    self.trigger = False

                self.pos = (hand_x - 0.5) * self.scale + 0.5

                if self.pos > 1 - self.len:
                    self.pos = 1 - self.len / 2
                if self.pos < 0 + self.len:
                    self.pos = self.len / 2

    def shoot(self):
        print("PLAYER: PEW!")
        self.bullets.append(Bullet(self.pos, 0.05))
        
class Bullet:
    def __init__(self, x, speed):
        self.x = x
        self.y = 1
        self.speed = speed
    
    def update(self):
        self.y -= self.speed

    def pos(self):
        return self.x, self.y
    