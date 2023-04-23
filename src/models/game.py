import numpy as np
import cv2
from my_utils.colors import *
import numpy as np
import random

class Game:
    def __init__(self, color=BLUE_RGB, alien_color=RED_RGB, scale=3, thickness=0.02):
        self.initialized = False
        self.w = None
        self.h = None
        self.pos = 0.5 # percentage of width
        self.thumb = None
        self.len = 0.1 # length of rectangel
        self.color = color
        self.thickness = thickness
        self.trigger = False
        self.alien_color=alien_color

        # scale up hand position so it doesn't need to move entire width of screen
        self.scale = scale 
        
        self.bullets = []
        self.aliens = [Alien()]

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
    
    def draw_aliens(self, frame):
        for alien in self.aliens:
            x, y, health = alien.state()

            if health <= 0:
                self.aliens.remove(alien) # remove bullet if off screen

            # draw alien
            frame = cv2.circle(frame, (int(x * self.w), int(y * self.h)), int(0.05 * self.w), 
                                  self.alien_color, thickness=-1) 
            
            for bullet in alien.bullets:
                x, y = bullet.pos()

                if x >= self.pos - self.len/2 and x <= self.pos + self.len/2 and y >= 1:
                    print("YOU LOST")
                    self.aliens.remove(alien)

                if y >= 1:
                    alien.bullets.remove(bullet) # remove bullet if off screen

                # draw bullet
                frame = cv2.rectangle(frame, (int(x * self.w), int(y * self.h)), 
                                    (int((x+0.01) * self.w), int((y+0.05) * self.h)), 
                                    self.alien_color, thickness=-1) 

                bullet.update() # update bullet position 

            if (alien.update(self.pos, self.len)):
                print("YOU LOST") # update alien state
                self.aliens.remove(alien)
        
        return frame

    def draw(self, frame):
        frame = cv2.rectangle(frame, (int(self.w * (self.pos - self.len / 2)), 
                                      int(self.h * (1 - self.thickness))), 
                                     (int(self.w * (self.pos + self.len / 2)), 
                                      int(self.h)), self.color, thickness=-1)  
        frame = self.draw_bullets(frame)
        frame = self.draw_aliens(frame)
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
    def __init__(self, x, speed, alien=False):
        self.x = x
        self.y = 1
        self.speed = speed
        self.alien = alien

        if alien:
            self.y = 0
    
    def update(self):
        if self.alien:
            self.y += self.speed
        else:
            self.y -= self.speed

    def pos(self):
        return self.x, self.y
    
class Alien:
    def __init__(self, speed=50, bullet_speed=0.03):
        self.health = 1
        self.x = random.uniform(0, 1)
        self.y = 0
        self.bullets = []
        self.count = 0
        self.speed = speed
        self.bullet_speed = bullet_speed

    def state(self):
        return self.x, self.y, self.health

    def update(self, pos, len):
        # shoot every self.speed frames
        self.count += 1

        if self.count == self.speed:
            self.shoot()
            self.count = 0

    def shoot(self):
        print("ALIEN: PEW!")
        self.bullets.append(Bullet(self.x, self.bullet_speed, True))