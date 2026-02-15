import pygame, sys
from game import button, settings, states, utils, constants





def main_menu(screen):
    pygame.display.set_caption("Menu")  
    main_menu_background = pygame.image.load("assets/backgrounds/start_screen_background.png")
    main_menu_background = pygame.transform.scale(main_menu_background, screen.get_size()).convert()

    sayovoltex_logo = pygame.image.load("assets/images/sayovoltex_logo.png").convert_alpha()
    sayovoltex_logo = pygame.transform.scale(sayovoltex_logo, (utils.scale_x(500), utils.scale_y(500)))

    play_button = button.Button(image=sayovoltex_logo, pos=(utils.scale_x(640), utils.scale_y(300)), 
                             text_input="", font=utils.get_font(utils.scale_y(constants.SIZE_MEDIUM_SMALL)), 
                             base_color="#d7fcd4", hovering_color="White")
    options_button = button.Button(image=None, pos=(utils.scale_x(640), utils.scale_y(600)), 
                                text_input="OPTIONS", font=utils.get_font(utils.scale_y(constants.SIZE_MEDIUM_SMALL)), 
                                base_color="#d7fcd4", hovering_color="White")
    quit_button = button.Button(image=None, pos=(utils.scale_x(1130), utils.scale_y(650)), 
                             text_input="QUIT", font=utils.get_font(utils.scale_y(constants.SIZE_MEDIUM_SMALL)),
                             base_color="#d7fcd4", hovering_color="White")
    editor_button = button.Button(image=None, pos=(utils.scale_x(150), utils.scale_y(650)), 
                             text_input="EDITOR", font=utils.get_font(utils.scale_y(constants.SIZE_MEDIUM_SMALL)),
                             base_color="#d7fcd4", hovering_color="White")

    # Load image assets for later
    utils.load_assets()    
    
    while True:
        screen.blit(main_menu_background, (0, 0))

        menu_mouse_pos = pygame.mouse.get_pos()


        
        for b in [play_button, options_button, quit_button, editor_button]:
            b.change_color(menu_mouse_pos)
            b.update(screen)

        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_button.check_for_input(menu_mouse_pos):
                    return states.PLAY
                elif options_button.check_for_input(menu_mouse_pos):
                    return states.OPTIONS
                elif quit_button.check_for_input(menu_mouse_pos):
                    return states.QUIT
                elif editor_button.check_for_input(menu_mouse_pos):
                    return states.EDITOR_INITIALIZE
        pygame.display.flip()






