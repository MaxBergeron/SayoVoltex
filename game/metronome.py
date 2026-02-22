import time
import threading
import pygame
from game import constants

class Metronome:
    def __init__(self, bpm, beats_per_bar):
        self.bpm = bpm
        self.beats_per_bar = beats_per_bar
        self.whistle_sound = pygame.mixer.Sound(constants.WHISTLE_SOUND_PATH)
        self.whistle_sound.set_volume(0.7)

        self.last_beat_index = -1

        self.beat_interval_ms = 60000 / bpm

    def update(self, current_audio_time_ms):
        if current_audio_time_ms >= 445:
            beat_index = int(current_audio_time_ms // self.beat_interval_ms)

            if beat_index > self.last_beat_index:
                self.last_beat_index = beat_index
                self.whistle_sound.play()
