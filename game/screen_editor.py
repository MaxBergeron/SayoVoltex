import os, sys
import pygame
from game import button, states, utils, constants, dropdown
import tkinter as tk



def editor_menu(screen, metadata=None, object_data=None):
    pygame.display.set_caption("Editor")

    main_menu_background = pygame.image.load("assets/backgrounds/editor_initialize_background.jpg").convert()
    main_menu_background = pygame.transform.scale(main_menu_background, screen.get_size()).convert()

    x_center = constants.BASE_W // 2
    y_center = constants.BASE_H // 2

    font_tiny = utils.get_font(utils.scale_y(constants.SIZE_TINY))
    font_xtiny = utils.get_font(utils.scale_y(constants.SIZE_XTINY))
    font_xxtiny = utils.get_font(utils.scale_y(constants.SIZE_XXTINY))

    map_lines_minimal = pygame.image.load("assets/images/map_lines_minimal.png")
    map_lines_minimal = pygame.transform.scale(map_lines_minimal, (utils.scale_x(400), utils.scale_y(720)))

    change_song_setup_dropdown = dropdown.Dropdown(
    0, 0, 200, 40, "Change Song Setup Settings",
    ["Title", "Artist", "Creator", "Version", "Scroll Speed", "BPM", "Audio Lead In"],
    font_xxtiny, font_tiny)

    note_button_image = pygame.image.load("assets/images/select_note_button.png")
    note_button_image = pygame.transform.scale(note_button_image, utils.scale_pos(150, 150))
    select_note_button = button.Button(image=note_button_image, pos=(utils.scale_x(100), utils.scale_y(250)), text_input="",
                                  font=utils.get_font(utils.scale_y(constants.SIZE_MEDIUM_SMALL)), base_color="#d7fcd4", hovering_color="White")
    laser_button_image = pygame.image.load("assets/images/select_laser_button.png")
    laser_button_image = pygame.transform.scale(laser_button_image, utils.scale_pos(150, 150))
    select_laser_button = button.Button(image=laser_button_image, pos=(utils.scale_x(100), utils.scale_y(450)), text_input="",
                                  font=utils.get_font(utils.scale_y(constants.SIZE_MEDIUM_SMALL)), base_color="#d7fcd4", hovering_color="White")

    

   
    while True:
        menu_mouse_pos = pygame.mouse.get_pos()
        event_list = pygame.event.get()

        screen.blit(main_menu_background, (0, 0))
        screen.blit(map_lines_minimal, utils.scale_pos((x_center - 200), 0))


        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return states.EDITOR_INITIALIZE
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if select_note_button.check_for_input(menu_mouse_pos):
                    print("Note button pressed")
                if select_laser_button.check_for_input(menu_mouse_pos):
                    print("Laser button pressed")

            change_song_setup_dropdown.handle_event(event, metadata)

        select_laser_button.update(screen)
        select_note_button.update(screen)
        change_song_setup_dropdown.draw(screen)
        pygame.display.flip()







