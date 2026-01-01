import pygame, sys
from game import button, states, utils, constants





def main_menu(screen):
    pygame.display.set_caption("Menu")  
    main_menu_background = pygame.image.load("assets/backgrounds/main_menu_background.jpg")
    main_menu_background = pygame.transform.scale(main_menu_background, screen.get_size()).convert()

    menu_text = utils.get_font(utils.scale_y(constants.SIZE_LARGE)).render("MAIN MENU", True, "#b68f40")
    menu_text_rect = menu_text.get_rect(center=(utils.scale_x(640), utils.scale_y(100)))

    play_button = button.Button(image=None, pos=(utils.scale_x(640), utils.scale_y(250)), 
                             text_input="PLAY", font=utils.get_font(utils.scale_y(constants.SIZE_MEDIUM)), 
                             base_color="#d7fcd4", hovering_color="White")
    options_button = button.Button(image=None, pos=(utils.scale_x(640), utils.scale_y(400)), 
                                text_input="OPTIONS", font=utils.get_font(utils.scale_y(constants.SIZE_MEDIUM)), 
                                base_color="#d7fcd4", hovering_color="White")
    quit_button = button.Button(image=None, pos=(utils.scale_x(640), utils.scale_y(550)), 
                             text_input="QUIT", font=utils.get_font(utils.scale_y(constants.SIZE_MEDIUM)),
                             base_color="#d7fcd4", hovering_color="White")
    
    # Load image assets for later
    utils.load_assets()
    
    while True:
        screen.blit(main_menu_background, (0, 0))

        menu_mouse_pos = pygame.mouse.get_pos()


        
        screen.blit(menu_text, menu_text_rect)

        for b in [play_button, options_button, quit_button]:
            b.change_color(menu_mouse_pos)
            b.update(screen)

        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_for_input(menu_mouse_pos):
                    return states.PLAY
                elif options_button.check_for_input(menu_mouse_pos):
                    return states.OPTIONS
                elif quit_button.check_for_input(menu_mouse_pos):
                    return states.QUIT
        pygame.display.flip()






