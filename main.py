from game import screen_editor_initialize, screen_main, screen_options, screen_play, screen_set_keybinds, screen_set_resolution, screen_map, screen_editor
from game import states, utils, constants
import pygame, sys

pygame.init()
screen = pygame.display.set_mode((constants.BASE_W, constants.BASE_H))
constants.SCALE_X = screen.get_width() / constants.BASE_W
constants.SCALE_Y = screen.get_height() / constants.BASE_H
print(f"Scale X: {constants.SCALE_X}, Scale Y: {constants.SCALE_Y}")


state = states.MENU
metadata, objectdata = None, None  

while True:
    result = None  

    if state == states.MENU:
        result = screen_main.main_menu(screen)

    elif state == states.OPTIONS:
        result = screen_options.options_menu(screen)
    elif state == states.SET_KEYBINDS:
        result = screen_set_keybinds.set_keybinds_menu(screen)
    elif state == states.SET_RESOLUTION:
        result = screen_set_resolution.set_resolution_menu(screen)

    elif state == states.PLAY:
        result = screen_play.play_menu(screen)
    elif state == states.MAP:
        result = screen_map.map_loader(screen)
        
    elif state == states.EDITOR_INITIALIZE:
        result = screen_editor_initialize.editor_initialize_menu(screen)
    elif state == states.EDITOR:
        result = screen_editor.editor_menu(screen, metadata, objectdata)  

    elif state == states.QUIT:
        pygame.quit()
        sys.exit()

    # Handle return values
    if isinstance(result, tuple):
        state, metadata, objectdata = result
    else:
        state = result

