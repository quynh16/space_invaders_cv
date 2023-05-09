import numpy as np
import cv2

from my_utils.colors import *
from .bullet import Bullet
from .alien import Alien

class Game:
    def __init__(self, player_color=BLUE_RGB, alien_color=RED_RGB, scale=2, height=0.02):
        '''Space invaders game where player controls the movement with their hand and shoots
        by retracting their thumb to their palm.
        '''

        self.initialized = False
        self.w = None # width of window
        self.h = None # height of window
        self.game_h = None

        # ============================= Gamplay Configuration ============================== #
        self.scale = scale # scale up hand position so it doesn't need to move the 
                           # entire width of the screen

        # ============================= Graphics Configuration ============================= #
        self.len = 0.1 # length of player sprite
        self.height = height # thickness of player's sprite 
        self.bottom_offset = 0.1
        self.player_color = player_color # color of player bar and bullets
        self.alien_len = 0.05 # length of alien sprite
        self.alien_color = alien_color # color of alien sprite
        self.bullet_w = 0.01
        self.bullet_h = 0.05
        
        # =============================== Game State Variables ============================= #
        # all values except "difficulty" are normalized values between 0 and 1, inclusive
        self.pos = 0.5 # position of player's index finger from 0 to 1
        self.thumb = None # position of player's thumb from 0 to 1
        self.trigger = False # whether thumb is in "trigger" state (to shoot)
        self.damage = 0.3 # damage we do
        self.alien_damage = 0.05  # damage aliens do
        self.health = 1
        self.count = 0 # counting frames to maintain game state and difficulty level
        self.difficulty = 100 # number of frames to wait until a new alien is generated
                              # so technically a smaller value == more difficult
        self.hit = False # used to draw us getting hit
        self.bullets = []
        self.aliens = [Alien(self.alien_len)] # initialize game with 1 alien
        self.points = 0
        self.in_game = True

    def update(self, frame, results):
        '''Processes hand tracking information and use it to draw the current frame.'''
        if not self.initialized:
            self.h, self.w = frame.shape[:2]
            self.game_h = int(self.h * (1 - self.bottom_offset))
            self.initialized = True

        frame = cv2.line(frame, (0, self.game_h), (self.w, self.game_h), self.player_color, thickness=1)

        if not self.in_game:
            if self.process_restart(results):
                self.restart_game()
                return self.draw(frame) # draw sprites on frame
            else:
                return self.losing_screen()
        elif self.health <= 0:
            return self.losing_screen()
        else:
            self.count += 1
            # generate a new alien every "difficulty" number of frames
            if self.count == self.difficulty:
                self.aliens.append(Alien(self.alien_len))
                self.count = 0

            self.process(results) # process hand tracking and update player position
            return self.draw(frame) # draw sprites on frame
        
    def restart_game(self):
        print("Restarting game.")
        self.in_game = True
        self.trigger = False # whether thumb is in "trigger" state (to shoot)
        self.health = 1
        self.count = 0 # counting frames to maintain game state and difficulty level
        self.difficulty = 100 # number of frames to wait until a new alien is generated
                              # so technically a smaller value == more difficult
        self.hit = False # used to draw us getting hit
        self.bullets = []
        self.aliens = [Alien(self.alien_len)] # initialize game with 1 alien
        self.points = 0
    
    def losing_screen(self):
        self.in_game = False

        # setup text
        font = cv2.FONT_HERSHEY_SIMPLEX
        text = "GAME OVER"

        # get boundary of this text
        textsize = cv2.getTextSize(text, font, 4, 4)[0]

        # get coords based on boundary
        textX = int((self.w - textsize[0]) / 2)
        textY = int((self.h + textsize[1]) / 2)

        # add text centered on image
        blank_image = np.zeros((self.h, self.w, 3), np.uint8)
        blank_image = cv2.putText(blank_image, text, (textX, textY), font, 4, WHITE_RGB, 4)

        # add a second line of text
        text = "PUT UP YOUR INDEX FINGER TO RESTART"

        # get coords based on boundary
        textX = int((self.w - cv2.getTextSize(text, font, 0.5, 2)[0][0]) / 2)
        textY = int(self.h * 0.8)

        # add text centered on image
        blank_image = cv2.putText(blank_image, text, (textX, textY), font, 0.5, WHITE_RGB, 2)

        return blank_image

    def draw(self, frame):
        '''Draws the sprites on the frame (e.g. player, bullets, aliens).'''
        frame = self.draw_bullets(frame)
        frame = self.draw_aliens(frame)

        # check if player hasn't lost due to alien reaching edge
        if self.in_game:
          frame = self.draw_player(frame)
          frame = self.draw_stats(frame)

        return frame
    
    def draw_player(self, frame):
        if self.hit:
            frame = cv2.rectangle(frame, (int(self.w * (self.pos - self.len / 2)), 
                                        int(self.game_h * (1 - self.height))), 
                                        (int(self.w * (self.pos + self.len / 2)), 
                                        int(self.game_h)), DARK_BLUE_RGB, thickness=-1)  
            self.hit = False
        else:
            frame = cv2.rectangle(frame, (int(self.w * (self.pos - self.len / 2)), 
                                        int(self.game_h * (1 - self.height))), 
                                        (int(self.w * (self.pos + self.len / 2)), 
                                        int(self.game_h)), self.player_color, thickness=-1)  
        
        return frame

    def draw_stats(self, frame):
        # Calculate the width of the bar based on the health value
        bar_width = int(self.health * 300)

        # Draw the background rectangle
        frame = cv2.rectangle(frame, (20 + bar_width, self.h - 50), (320, self.h - 20), RED_RGB, -1)

        # Draw the bar
        if self.health > 0:
            frame = cv2.rectangle(frame, (20, self.h - 50), (20 + bar_width, self.h - 20), GREEN_RGB, -1)

        text = f"POINTS: {self.points}"
        frame = cv2.putText(frame, text, (770, self.h - 25), cv2.FONT_HERSHEY_SIMPLEX,
                            1, BLACK_RGB, 2, cv2.LINE_AA)
        return frame

    def draw_bullets(self, frame):
        '''Draw the player's bullets on the frame.'''
        for bullet in self.bullets:
            x, y = bullet.pos()
            hit = False
            
            # check if our bullet hit any aliens
            for alien in self.aliens:
                alien_x, alien_y = alien.state()[:2]

                if alien_y - self.alien_len < y < alien_y + self.alien_len and (
                      alien_x - self.alien_len < x < alien_x + self.alien_len):
                    if (alien.get_hit(self.damage)): # if hit kills alien, remove it from list
                        self.aliens.remove(alien)
                        self.points +=1 # and increase point by 1

                    hit = True
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                elif y <= 0 and bullet in self.bullets:
                    self.bullets.remove(bullet) # remove bullet if it goes off screen

            # draw bullet
            if not hit:
                frame = cv2.rectangle(frame, (int((x - self.bullet_w / 2) * self.w), 
                                              int((y - self.bullet_h) * self.game_h)), 
                                             (int((x + self.bullet_w / 2) * self.w), 
                                              int((y) * self.game_h)), 
                                              self.player_color, thickness=-1) 

            bullet.update() # update bullet position 
        
        return frame
    
    def draw_aliens(self, frame):
        '''Draws the aliens on the current frame.'''
        for alien in self.aliens:
            x, y, is_hit = alien.state()

            if y >= 1:
                return self.losing_screen()

            # draw alien as a darker red if it just got hit
            if is_hit:
                frame = cv2.circle(frame, (int(x * self.w), 
                                           int((y - self.alien_len) * self.game_h)), 
                                           int(self.alien_len * self.game_h * 1.5), 
                                           DARK_RED_RGB, thickness=-1) 
            else:
                frame = cv2.circle(frame, (int(x * self.w), 
                                           int((y - self.alien_len) * self.game_h)), 
                                           int(self.alien_len * self.game_h * 1.5), 
                                           self.alien_color, thickness=-1) 
            
            # draw alien's bullets
            for bullet in alien.bullets:
                x, y = bullet.pos()
                hit = False

                # check if alien bullets hit us
                if x >= self.pos - self.len/2 and x <= self.pos + self.len/2 and y >= 1-self.height:
                    self.get_hit()
                    alien.bullets.remove(bullet)
                    hit = True
                elif y - self.bullet_h >= 1:
                    alien.bullets.remove(bullet) # remove bullet if off screen

                # draw bullet if it didn't hit us
                if not hit and y - self.bullet_h < 1:
                    end = y if y < 1 else 1
                    frame = cv2.rectangle(frame, (int((x - self.bullet_w / 2) * self.w), 
                                                  int((y - self.bullet_h) * self.game_h)), 
                                                 (int((x + self.bullet_w / 2) * self.w), 
                                                  int((end) * self.game_h)), 
                                                  self.alien_color, thickness=-1) 

                    bullet.update() # update bullet position 

            alien.update() # update alien state
    
        return frame
    
    def shoot(self):
        '''Action to take when player shoots.'''
        print("PLAYER: PEW!")
        self.bullets.append(Bullet(self.pos, 1, 0.05))

    def get_hit(self):
        self.health -= self.alien_damage
        self.hit = True

    def process_restart(self, results):
        restart = False
        if results.multi_hand_landmarks:
            handedness = results.multi_handedness[0].classification[0].label
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks = hand_landmarks.landmark
                restart = bool(landmarks[8].y < landmarks[6].y)
                if handedness == 'Right':
                    restart = restart and landmarks[4].x > landmarks[3].x   #Right Thumb
                else:
                    restart = restart and landmarks[4].x < landmarks[3].x   #Left Thumb
                restart = restart and landmarks[12].y > landmarks[10].y    #Middle finger
                restart = restart and landmarks[16].y > landmarks[14].y     #Ring finger
                restart = restart and landmarks[20].y > landmarks[18].y     #Little finger

                if restart:
                    print("Processing restart!")
                    return True
                    
        return restart

    def process(self, results):
        '''Detect hand position to determine player's position and whether they shot.'''
        if results.multi_hand_landmarks:
            handedness = results.multi_handedness[0].classification[0].label
            for hand_landmarks in results.multi_hand_landmarks:
                hand_x = hand_landmarks.landmark[8].x

                # detect thumb closed, don't shoot until release
                self.thumb = hand_landmarks.landmark[4].x
                self.thumb_thresh = hand_landmarks.landmark[5].x

                if handedness == 'Right':
                    if self.thumb > self.thumb_thresh:
                        self.trigger = True

                    # shoot upon thumb release
                    if self.trigger and self.thumb < self.thumb_thresh:
                        self.shoot()
                        self.trigger = False
                else:
                    if self.thumb < self.thumb_thresh:
                        self.trigger = True

                    # shoot upon thumb release
                    if self.trigger and self.thumb > self.thumb_thresh:
                        self.shoot()
                        self.trigger = False

                # update player position
                self.pos = (hand_x - 0.5) * self.scale + 0.5

                # don't let player's sprite go off screen
                if self.pos > 1 - self.len / 2:
                    self.pos = 1 - self.len / 2
                if self.pos < 0 + self.len / 2:
                    self.pos = self.len / 2