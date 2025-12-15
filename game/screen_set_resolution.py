import pygame, sys
from game import button, constants, states, utils

def set_resolution_menu(screen):
    pygame.display.set_caption("Set Resolution")
    set_resolution_background = pygame.image.load("assets/set_resolution_background.png")
    set_resolution_background = pygame.transform.scale(set_resolution_background, screen.get_size()).convert()

    waiting_for_selection = False
    last_screen_size = screen.get_size()

    while True:
        current_size = screen.get_size()
        if current_size != last_screen_size:
            current_size = screen.get_size()
            set_resolution_background = pygame.transform.scale(set_resolution_background, current_size)

            last_screen_size = current_size
        screen.blit(set_resolution_background, (0, 0)) 

        set_resolution_mouse_pos = pygame.mouse.get_pos()

        popup_width, popup_height = utils.scale_x(450), utils.scale_y(400)
        popup_x = (screen.get_width() - popup_width) // 2
        popup_y = (screen.get_height() - popup_height) // 2
        popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)

        set_resolution_text = utils.get_font(utils.scale_y(constants.SIZE_LARGE)).render("SET RESOLUTION", True, "#b68f40")
        set_resolution_text_rect = set_resolution_text.get_rect(center=(utils.scale_x(640), utils.scale_y(100)))

        back_button = button.Button(image=None, pos=(utils.scale_x(150), utils.scale_y(650)), 
                             text_input="Back", font=utils.get_font(utils.scale_y(constants.SIZE_MEDIUM_SMALL)), 
                             base_color="#d7fcd4", hovering_color="White")
        change_resolution_button = button.Button(image=None, pos=(utils.scale_x(640), utils.scale_y(350)), 
                             text_input="Change Resolution", font=utils.get_font(utils.scale_y(constants.SIZE_MEDIUM_SMALL)), 
                             base_color="#d7fcd4", hovering_color="White")
        full_screen_button = button.Button(image=None, pos=(utils.scale_x(640), utils.scale_y(450)), 
                             text_input="Fullscreen", font=utils.get_font(utils.scale_y(constants.SIZE_MEDIUM_SMALL)), 
                             base_color="#d7fcd4", hovering_color="White")
        resolution_buttons = [
            button.Button(image=None, pos=(popup_x + popup_width // 2, popup_y + utils.scale_y(150)), 
                             text_input="1280x720", font=utils.get_font(utils.scale_y(constants.SIZE_SMALL)), 
                             base_color="#d7fcd4", hovering_color="White"),
            button.Button(image=None, pos=(popup_x + popup_width // 2, popup_y + utils.scale_y(250)), 
                             text_input="1920x1080", font=utils.get_font(utils.scale_y(constants.SIZE_SMALL)), 
                             base_color="#d7fcd4", hovering_color="White"),
            button.Button(image=None, pos=(popup_x + popup_width // 2, popup_y + utils.scale_y(350)), 
                             text_input="2560x1440", font=utils.get_font(utils.scale_y(constants.SIZE_SMALL)), 
                             base_color="#d7fcd4", hovering_color="White")
        ]
        
        screen.blit(set_resolution_text, set_resolution_text_rect)

        for b in [back_button, change_resolution_button, full_screen_button]:
            b.change_color(set_resolution_mouse_pos)
            b.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.check_for_input(set_resolution_mouse_pos):
                    return states.OPTIONS
                if change_resolution_button.check_for_input(set_resolution_mouse_pos):
                    waiting_for_selection = True
                if full_screen_button.check_for_input(set_resolution_mouse_pos):
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    constants.SCALE_X = screen.get_width() / constants.BASE_W
                    constants.SCALE_Y = screen.get_height() / constants.BASE_H
                if resolution_buttons[0].check_for_input(set_resolution_mouse_pos):
                    screen = pygame.display.set_mode((1280, 720))
                    constants.SCALE_X = 1280 / constants.BASE_W
                    constants.SCALE_Y = 720 / constants.BASE_H
                    waiting_for_selection = False
                if resolution_buttons[1].check_for_input(set_resolution_mouse_pos):
                    screen = pygame.display.set_mode((1920, 1080))
                    constants.SCALE_X = 1920 / constants.BASE_W
                    constants.SCALE_Y = 1080 / constants.BASE_H
                    waiting_for_selection = False
                if resolution_buttons[2].check_for_input(set_resolution_mouse_pos):
                    screen = pygame.display.set_mode((2560, 1440))
                    constants.SCALE_X = 2560 / constants.BASE_W
                    constants.SCALE_Y = 1440 / constants.BASE_H
                    waiting_for_selection = False

            if event.type == pygame.KEYDOWN:
                if waiting_for_selection:
                    if event.key == pygame.K_ESCAPE:
                        waiting_for_selection = False  
                else:
                    if event.key == pygame.K_ESCAPE:
                        return states.MENU
                    
        if waiting_for_selection:
            change_resolution_popup(screen, set_resolution_mouse_pos, popup_rect, resolution_buttons)
                
        pygame.display.flip()

def change_resolution_popup(screen, set_resolution_mouse_pos, popup_rect, resolution_buttons):

    pygame.draw.rect(screen, (50, 50, 50), popup_rect)
    pygame.draw.rect(screen, (255, 255, 255), popup_rect, 2)

    prompt_text = utils.get_font(constants.SIZE_TINY).render("Select resolution", True, (255, 255, 255))
    prompt_rect = prompt_text.get_rect(midtop=(popup_rect.centerx, popup_rect.top + utils.scale_y(20)))

    screen.blit(prompt_text, prompt_rect)

    for b in resolution_buttons:
        b.change_color(set_resolution_mouse_pos)
        b.update(screen)


    