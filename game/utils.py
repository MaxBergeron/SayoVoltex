import pygame
from game import constants


key_bindings = {
    "key_1": pygame.K_z,
    "key_2": pygame.K_x,
    "key_3": pygame.K_c,
    "key_CCW": pygame.K_q,    
    "key_CW": pygame.K_w,
}

def set_keybinding(action, key):
    key_bindings[action] = key

def get_font(size): 
    return pygame.font.Font("assets/font/font.ttf", int(size))

def scale_x(num):
    return int(num * constants.SCALE_X)
def scale_y(num):
    return int(num * constants.SCALE_Y)
def scale_pos(x, y):
    return int(x * constants.SCALE_X), int(y * constants.SCALE_Y)
def scale_size(width, height):
    return int(width * constants.SCALE_X), int(height * constants.SCALE_Y)