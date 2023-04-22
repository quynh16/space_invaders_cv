import numpy as np

class Game:
    # Game table assumes table size is 100 x 100 
    def __init__(self):
        self.puck = np.array([50, 50]) # initialize puck to center of table
        self.p1 = np.array([25, 50])
        self.p2 = np.array([75, 50])