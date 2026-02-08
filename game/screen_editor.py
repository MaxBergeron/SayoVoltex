import os, sys
import pygame
from game import button, states, utils, constants, dropdown, note_tool, timeline, screen_editor_initialize
import tkinter as tk



def editor_menu(screen, metadata=None, object_data=None):
    pygame.display.set_caption("Editor")
    pygame.key.set_repeat(300, 50)

    main_menu_background = pygame.image.load("assets/backgrounds/editor_initialize_background.jpg").convert()
    main_menu_background = pygame.transform.scale(main_menu_background, screen.get_size()).convert()

    x_center = constants.BASE_W // 2
    y_center = constants.BASE_H // 2

    font_tiny = utils.get_font(utils.scale_y(constants.SIZE_TINY))
    font_xtiny = utils.get_font(utils.scale_y(constants.SIZE_XTINY))
    font_xxtiny = utils.get_font(utils.scale_y(constants.SIZE_XXTINY))

    constants.SCROLL_SPEED = float(metadata["Scroll Speed"])
    audio_length_ms = screen_editor_initialize.get_audio_length(metadata["Audio Path"]) * 1000
    time_line = timeline.Timeline(audio_length_ms)

    map_lines_minimal = pygame.image.load("assets/images/map_lines_minimal.png")
    map_lines_minimal = pygame.transform.scale(map_lines_minimal, (utils.scale_x(400), utils.scale_y(720)))

    editor_grid = note_tool.NoteTool()
    editor_grid.add_breakpoint(int(metadata["Audio Lead In"]))

    temp_note_storage = []

    change_song_setup_dropdown = dropdown.Dropdown(
    0, 0, 200, 40, "Change Song Setup Settings",
    ["Title", "Artist", "Creator", "Version", "Scroll Speed", "BPM", "Audio Lead In"],
    font_xxtiny, font_tiny, True)

    beat_divisor_value = {"value": "1/4"}
    choose_beat_division_dropdown = dropdown.Dropdown(
    200, 0, 200, 40, "Choose Beat Division",
    ["1/4", "1/8", "1/12", "1/16", "1/24", "1/32"],
    font_xxtiny, font_tiny, False)


    add_breakpoint_button = button.Button(image=None, pos=(utils.scale_x(1060), utils.scale_y(18)), text_input="+",
                                  font=utils.get_font(utils.scale_y(constants.SIZE_SMALL)), base_color="#a1a1a1", hovering_color="White")
    breakpoints_dropdown = dropdown.Dropdown(
    1080, 0, 200, 40, "Breakpoints",
    editor_grid.get_breakpoints(),
    font_xxtiny, font_tiny, True)

    note_button_image = pygame.image.load("assets/images/select_note_button.png")
    note_button_image = pygame.transform.scale(note_button_image, utils.scale_pos(150, 150))
    select_note_button = button.Button(image=note_button_image, pos=(utils.scale_x(100), utils.scale_y(250)), text_input="",
                                  font=utils.get_font(utils.scale_y(constants.SIZE_MEDIUM_SMALL)), base_color="#d7fcd4", hovering_color="White")
    laser_button_image = pygame.image.load("assets/images/select_laser_button.png")
    laser_button_image = pygame.transform.scale(laser_button_image, utils.scale_pos(150, 150))
    select_laser_button = button.Button(image=laser_button_image, pos=(utils.scale_x(100), utils.scale_y(450)), text_input="",
                                  font=utils.get_font(utils.scale_y(constants.SIZE_MEDIUM_SMALL)), base_color="#d7fcd4", hovering_color="White")

    

    editor_time_ms = 0

    while True:
        menu_mouse_pos = pygame.mouse.get_pos()
        event_list = pygame.event.get()

        screen.blit(main_menu_background, (0, 0))
        editor_grid.draw_background(screen)
        editor_grid.draw_notes(screen, editor_time_ms)
        screen.blit(map_lines_minimal, utils.scale_pos((x_center - 200), 0))




        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not change_song_setup_dropdown.input_active and not breakpoints_dropdown.input_active:
                    return states.EDITOR_INITIALIZE
                # Redo
                if event.key == pygame.K_z and (event.mod & pygame.KMOD_CTRL) and (event.mod & pygame.KMOD_SHIFT):
                    if temp_note_storage:
                        editor_grid.notes.append(temp_note_storage.pop())
                # Undo
                elif event.key == pygame.K_z and (event.mod & pygame.KMOD_CTRL):
                    if editor_grid.notes:
                        temp_note_storage.append(editor_grid.notes.pop())
                # Delete last
                elif event.key == pygame.K_BACKSPACE:
                    if editor_grid.notes:
                        temp_note_storage.append(editor_grid.notes.pop())
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked_note = editor_grid.get_note_at_click(menu_mouse_pos, editor_time_ms)
                if select_note_button.check_for_input(menu_mouse_pos):
                    if editor_grid.object_place_type == "note":
                        editor_grid.object_place_type = None
                    else:
                        editor_grid.object_place_type = "note"                
                elif select_laser_button.check_for_input(menu_mouse_pos):
                    if editor_grid.object_place_type == "laser":
                        editor_grid.object_place_type = None
                    else:
                        editor_grid.object_place_type = "laser"  
                elif add_breakpoint_button.check_for_input(menu_mouse_pos):
                    breakpoints_dropdown.start_add_breakpoint_prompt()
                    breakpoints_dropdown.handle_event(event, metadata, editor_grid)
                elif (clicked_info := time_line.check_for_input(menu_mouse_pos))[0]:
                    editor_time_ms = time_line.update(clicked_info[1])
                elif editor_grid.check_for_input(menu_mouse_pos, editor_time_ms, metadata["BPM"], beat_divisor_value["value"]):
                    pass
            elif event.type == pygame.MOUSEWHEEL:
                if editor_grid.in_bounds(menu_mouse_pos):
                    if editor_time_ms + event.y * 200 >= 0 and editor_time_ms + event.y * 200 <= audio_length_ms:
                        editor_time_ms += event.y * 200
                        time_line.update(editor_time_ms / audio_length_ms * constants.BASE_W)



            change_song_setup_dropdown.handle_event(event, metadata)
            choose_beat_division_dropdown.handle_event(event, beat_divisor_value)
            breakpoints_dropdown.handle_event(event, {"value": editor_grid.get_breakpoints()}, editor_grid)

        
        time_line.draw(screen)
        editor_grid.draw_note_hover(screen, menu_mouse_pos, editor_time_ms, metadata["BPM"], beat_divisor_value["value"])
        select_laser_button.update(screen)
        select_note_button.update(screen)
        change_song_setup_dropdown.draw(screen)
        choose_beat_division_dropdown.draw(screen)
        breakpoints_dropdown.draw(screen)
        add_breakpoint_button.update(screen)
        add_breakpoint_button.change_color(menu_mouse_pos)
        pygame.display.flip()







