import pygame, sys
from game import button, states, utils, constants



def play_menu(screen):
    pygame.display.set_caption("Play")
    play_background = pygame.image.load("assets/play_background.jpg")
    play_background = pygame.transform.scale(play_background, screen.get_size()).convert()

    while True:
        screen.blit(play_background, (0, 0))
        play_mouse_pos = pygame.mouse.get_pos()

        play_text = utils.get_font(utils.scale_y(constants.SIZE_LARGE)).render("Play", True, "#b68f40")
        play_text_rect = play_text.get_rect(center=(utils.scale_x(640), utils.scale_y(100)))

        back_button = button.Button(image=None, pos=(utils.scale_x(150), utils.scale_y(650)), 
                             text_input="Back", font=utils.get_font(utils.scale_y(constants.SIZE_MEDIUM_SMALL)), 
                             base_color="#d7fcd4", hovering_color="White")
        
        screen.blit(play_text, play_text_rect)

        for b in [back_button]:
            b.change_color(play_mouse_pos)
            b.update(screen)

        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.check_for_input(play_mouse_pos):
                    return states.MENU
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return states.MENU

        pygame.display.flip()