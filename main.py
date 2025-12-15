from game import screen_main, screen_options, screen_play, screen_set_keybinds
from game import states, utils, constants
import pygame, sys

pygame.init()
#screen = pygame.display.set_mode((constants.BASE_W, constants.BASE_H))
screen = pygame.display.set_mode((1920, 1080))
constants.SCALE_X = screen.get_width() / constants.BASE_W
constants.SCALE_Y = screen.get_height() / constants.BASE_H
print(f"Scale X: {constants.SCALE_X}, Scale Y: {constants.SCALE_Y}")


state = states.MENU

while True:
    if state == states.MENU:
        state = screen_main.main_menu(screen)

    elif state == states.OPTIONS:
        state = screen_options.options_menu(screen)
    elif state == states.SET_KEYBINDS:
        state = screen_set_keybinds.set_keybinds_menu(screen)
        
    elif state == states.PLAY:
        state = screen_play.play_menu(screen)

    elif state == states.QUIT:
        pygame.quit()
        sys.exit()
