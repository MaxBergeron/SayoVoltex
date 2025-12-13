import pygame


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
    return pygame.font.Font("assets/font/font.ttf", size)
