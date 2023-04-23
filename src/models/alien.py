import random
from .bullet import Bullet

class Alien:
    '''Tracks the state of a single alien.'''
    def __init__(self, width=0.05, speed=70, bullet_speed=0.03):
        self.health = 1
        self.x = random.uniform(width, 1-width) # need to account for alien width
        self.y = 0
        self.bullets = []
        self.count = 0 # used to count number of frames passed
        self.speed = speed # number of frames to wait before shooting again
        self.bullet_speed = bullet_speed # how fast the bullet moves
        self.hit = False # whether the alien has just been hit. need this to
                         # draw the alien in a darker color to indicate it was hit

    def state(self):
        return self.x, self.y, self.hit

    def update(self):
        # shoot every self.speed frames
        self.count += 1

        # shoot every "speed" number of frames
        if self.count == self.speed:
            self.shoot()
            self.count = 0

        # show aliens getting hit for hit_frames number of frames
        if self.hit:
            self.hit = False

    def shoot(self):
        print("ALIEN: PEW!")
        self.bullets.append(Bullet(self.x, self.bullet_speed, True))

    def get_hit(self, damage):
        # returns true if alien dies from this attack
        self.health -= damage
        self.hit = True

        if (self.health <= 0):
            return True
        
        return False