from game import screen_editor_initialize, screen_main, screen_options, screen_play, screen_set_keybinds, screen_set_resolution, screen_map, screen_editor, settings, screen_map_complete, screen_audio_settings
from game import states, utils, constants
import pygame, sys, gc

pygame.init()
pygame.mixer.init()
print(pygame.mixer.get_init())
gc.disable()
game_settings = settings.load_settings()
screen = pygame.display.set_mode((game_settings["resolution"][0], game_settings["resolution"][1]), pygame.FULLSCREEN if game_settings["fullscreen"] else 0)
pygame.scrap.init()
constants.SCALE_X = screen.get_width() / constants.BASE_W
constants.SCALE_Y = screen.get_height() / constants.BASE_H
print(f"Scale X: {constants.SCALE_X}, Scale Y: {constants.SCALE_Y}")


state = states.MENU
metadata, objectdata, map_path = None, None, None
counters = None

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
    elif state == states.AUDIO_SETTINGS:
        result = screen_audio_settings.audio_settings_menu(screen)

    elif state == states.PLAY:
        result = screen_play.play_menu(screen)
    elif state == states.MAP:
        result = screen_map.map_loader(screen)
    elif state == states.MAP_COMPLETE:
        result = screen_map_complete.map_complete_menu(screen, counters)
        
    elif state == states.EDITOR_INITIALIZE:
        result = screen_editor_initialize.editor_initialize_menu(screen)
    elif state == states.EDITOR:
            result = screen_editor.editor_menu(screen, metadata, objectdata, map_path)  

    elif state == states.QUIT:
        pygame.quit()
        sys.exit()

    if isinstance(result, tuple):

        if len(result) == 2:
            state, counters = result

        elif len(result) == 4:
            state, metadata, objectdata, map_path = result

    else:
        state = result

