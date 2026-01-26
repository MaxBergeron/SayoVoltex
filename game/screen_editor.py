import os, sys
import pygame
from game import button, states, utils, constants, dropdown
import tkinter as tk



def editor_menu(screen, metadata=None, object_data=None):
    pygame.display.set_caption("Editor")

    main_menu_background = pygame.image.load("assets/backgrounds/editor_initialize_background.jpg").convert()
    main_menu_background = pygame.transform.scale(main_menu_background, screen.get_size()).convert()
    font_tiny = utils.get_font(utils.scale_y(constants.SIZE_TINY))
    font_xtiny = utils.get_font(utils.scale_y(constants.SIZE_XTINY))
    font_xxtiny = utils.get_font(utils.scale_y(constants.SIZE_XXTINY))

    change_song_setup_dropdown = dropdown.Dropdown(
    0, 0, 200, 40, "Change Song Setup Settings",
    ["Title", "Artist", "Creator", "Version", "Scroll Speed", "BPM", "Audio Lead In"],
    font_xxtiny, font_tiny)
    

   
    while True:
        menu_mouse_pos = pygame.mouse.get_pos()
        event_list = pygame.event.get()

        screen.blit(main_menu_background, (0, 0))


        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            change_song_setup_dropdown.handle_event(event, metadata)
            print(metadata)

        change_song_setup_dropdown.draw(screen)
        pygame.display.flip()







