import pygame
from game import utils, constants

class PointCounter:
    def __init__(self):
        self.value = 0
        self.font = utils.get_font(utils.scale_y(constants.SIZE_TINY))
        self.position_x = utils.scale_x(15)
        self.position_y = utils.scale_y(5)
        self.update_text_surface()

    def update_text_surface(self):
        self.text = self.font.render(str(self.value), True, (255, 255, 255))  # White color

  
    def update(self, screen):
        screen.blit(self.text, (self.position_x, self.position_y))




class PercentageCounter:
    def __init__(self):
        self.value = 0.0
        self.total_percent = 0.0
        self.total_hits = 0
        self.font = utils.get_font(utils.scale_y(constants.SIZE_TINY))
        self.position_x = utils.scale_x(15)
        self.position_y = utils.scale_y(45)
        self.update_text_surface()

    def add_hit(self, hit_percent):
        self.total_hits += 1
        self.total_percent += hit_percent
        self.value = self.total_percent / self.total_hits
        self.update_text_surface()

    def update_text_surface(self):
        self.text = self.font.render(f"{self.value:.1f}%", True, (255, 255, 255))

    def update(self, screen):
        screen.blit(self.text, (self.position_x, self.position_y))




class ComboCounter:
    def __init__(self):
        self.value = 0
        self.font = utils.get_font(utils.scale_y(constants.SIZE_SMALL))
        self.position_x = utils.scale_x(1000)
        self.position_y = utils.scale_y(5)
        self.update_text_surface()

    def update_text_surface(self):
        text_str = f"{self.value}x Combo"
        self.text = self.font.render(text_str, True, (255, 255, 0))

  
    def update(self, screen):
        screen.blit(self.text, (self.position_x, self.position_y))
