import os, sys
import pygame
from game import button, states, utils, constants



def editor_menu(screen, metadata=None, object_data=None):
    pygame.display.set_caption("Editor")

    main_menu_background = pygame.image.load("assets/backgrounds/editor_initialize_background.jpg").convert()
    main_menu_background = pygame.transform.scale(main_menu_background, screen.get_size()).convert()

    font_xtiny = utils.get_font(utils.scale_y(constants.SIZE_XTINY))
    
   
    while True:
        menu_mouse_pos = pygame.mouse.get_pos()
        event_list = pygame.event.get()

        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        screen.blit(main_menu_background, (0, 0))
        pygame.display.flip()
