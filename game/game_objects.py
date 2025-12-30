import pygame
from game import constants, utils

class HitObject:
    def __init__(self, key, duration, time):
        self.key = int(key)
        self.duration = float(duration)
        self.time = float(time)
        self.hit = False
        self.miss = False
        self.position_x = 0
        self.hold_started = False
        self.holding = False
        self.hold_complete = False

    def __repr__(self):
        return f"HitObject(key={self.key}, duration={self.duration}, time={self.time})"


class LaserObject:
    def __init__(self, continue_chain, full_swing, position, time):
        self.continue_chain = bool(int(continue_chain))
        self.full_swing = int(full_swing)
        self.position = int(position)
        self.time = float(time)
 
    def __repr__(self):
        return f"LaserObject(chain={self.continue_chain}, pos={self.position}, time={self.time})"