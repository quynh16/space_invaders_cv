class Bullet:
    '''Tracks the state of a single bullet.'''
    def __init__(self, x, y, speed, alien=False):
        self.x = x
        self.y = y
        self.speed = speed
        self.alien = alien
    
    def update(self):
        if self.alien:
            self.y += self.speed
        else:
            self.y -= self.speed

    def pos(self):
        return self.x, self.y