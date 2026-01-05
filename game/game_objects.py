import pygame
from game import constants, utils

class HitObject:
    def __init__(self, key, duration, time):
        self.key = int(key)
        self.duration = int(duration)
        self.time = int(time)
        self.hit = False
        self.miss = False
        self.position_x = 0
        self.hold_started = False
        self.holding = False
        self.hold_complete = False

class LaserObject:
    def __init__(self, start_time, end_time, start_pos, end_pos):
        self.start_time = int(start_time)
        self.end_time = int(end_time)
        self.start_pos = float(LaserObject.normalize_position(int(start_pos)))
        self.end_pos = float(LaserObject.normalize_position(int(end_pos)))
        self.hit = False

    def normalize_position(pos):
        norm_pos = (pos - 1) / 7
        return norm_pos