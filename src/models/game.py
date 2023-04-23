import numpy as np
import cv2
from my_utils.colors import *
import numpy as np
from .bullet import Bullet
from .alien import Alien

class Game:
    def __init__(self, player_color=BLUE_RGB, alien_color=RED_RGB, scale=2, height=0.02):
        self.initialized = False
        self.w = None # width of window
        self.h = None # height of window

        # ============================= Gamplay Configuration ============================== #
        self.scale = scale # scale up hand position so it doesn't need to move the 
                           # entire width of the screen

        # ============================= Graphics Configuration ============================= #
        self.len = 0.1 # length of player sprite
        self.height = height # thickness of player's sprite 
        self.player_color = player_color # color of player bar and bullets
        self.alien_len = 0.05 # length of alien sprite
        self.alien_color = alien_color # color of alien sprite
        
        # =============================== Game State Variables ============================= #
        self.pos = 0.5 # position of player's index finger from 0 to 1
        self.thumb = None # position of player's thumb from 0 to 1
        self.trigger = False # whether thumb is in "trigger" state (to shoot)
        self.damage = 0.3 # damage we do
        self.alien_damage = 0.1 # damage aliens do
        self.health = 1
        self.count = 0 # counting frames to maintain game state and difficulty level
        self.difficulty = 100 # number of frames to wait until a new alien is generated
                              # so technically a smaller value == more difficult
        self.bullets = []
        self.aliens = [Alien(self.width)]

    def update(self, frame, results):
        '''Processes hand tracking information and use it to draw the current frame.'''
        if not self.initialized:
            self.h, self.w = frame.shape[:2]
            self.initialized = True

        self.count += 1
        # generate a new alien every "difficulty" number of frames
        if self.count == self.difficulty:
            self.aliens.append(Alien(self.width))
            self.count = 0

        print("NUMBER OF BULLETS:", len(self.bullets))

        self.process(results) # process hand tracking and update player position
        return self.draw(frame) # draw sprites on frame
    
    def draw(self, frame):
        '''Draws the sprites on the frame (e.g. player, bullets, aliens).'''
        frame = cv2.rectangle(frame, (int(self.w * (self.pos - self.len / 2)), 
                                      int(self.h * (1 - self.height))), 
                                     (int(self.w * (self.pos + self.len / 2)), 
                                      int(self.h)), self.player_color, thickness=-1)  
        frame = self.draw_bullets(frame)
        frame = self.draw_aliens(frame)
        return frame
    
    def draw_bullets(self, frame):
        '''Draw the player's bullets on the frame.'''
        for bullet in self.bullets:
            x, y = bullet.pos()
            
            # check if bullet hit any aliens
            for alien in self.aliens:
                alien_x = alien.state()[0]

                if y <= 0 and x > alien_x - self.alien_len and x < alien_x + self.alien_len:
                    if (alien.get_hit(self.damage)): # if hit kills alien, remove it from list
                        self.aliens.remove(alien)

                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    break
                elif y <= 0 and bullet in self.bullets:
                    self.bullets.remove(bullet) # remove bullet if it goes off screen

            # draw bullet
            frame = cv2.rectangle(frame, (int(x * self.w), int(y * self.h)), 
                                (int((x+0.01) * self.w), int((y+0.05) * self.h)), 
                                self.player_color, thickness=-1) 

            bullet.update() # update bullet position 
        
        return frame
    
    def draw_aliens(self, frame):
        '''Draws the aliens on the current frame.'''
        for alien in self.aliens:
            x, y, hit = alien.state()

            # draw alien as a darker red if it just got hit
            if hit:
                frame = cv2.circle(frame, (int(x * self.w), int(y * self.h)), 
                               int(self.alien_len * self.w), 
                               (0,0,0), thickness=-1) 
            else:
                frame = cv2.circle(frame, (int(x * self.w), int(y * self.h)), 
                                int(self.alien_len * self.w), 
                                self.alien_color, thickness=-1) 
            
            # draw alien's bullets
            for bullet in alien.bullets:
                x, y = bullet.pos()

                if x >= self.pos - self.len/2 and x <= self.pos + self.len/2 and y >= 1:
                    print("YOU LOST")

                if y >= 1:
                    alien.bullets.remove(bullet) # remove bullet if off screen

                # draw bullet
                frame = cv2.rectangle(frame, (int(x * self.w), int(y * self.h)), 
                                     (int((x+0.01) * self.w), int((y+0.05) * self.h)), 
                                      self.alien_color, thickness=-1) 

                bullet.update() # update bullet position 

            alien.update() # update alien state
    
        return frame

    def process(self, results):
        '''Detect hand position to determine player's position and whether they shot.'''
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                hand_x = hand_landmarks.landmark[8].x
                self.thumb = hand_landmarks.landmark[4].x

                # detect thumb closed, don't shoot until release
                self.thumb_thresh = hand_landmarks.landmark[5].x
                if self.thumb > self.thumb_thresh:
                    self.trigger = True
                
                # shoot upon thumb release
                if self.trigger and self.thumb < self.thumb_thresh:
                    self.shoot()
                    self.trigger = False

                # update player position
                self.pos = (hand_x - 0.5) * self.scale + 0.5

                # don't let player's sprite go off screen
                if self.pos > 1 - self.len:
                    self.pos = 1 - self.len / 2
                if self.pos < 0 + self.len:
                    self.pos = self.len / 2

    def shoot(self):
        '''Action to take when player shoots.'''
        print("PLAYER: PEW!")
        self.bullets.append(Bullet(self.pos, 0.05))