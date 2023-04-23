class Bullet:
    '''Tracks the state of a single bullet.'''
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