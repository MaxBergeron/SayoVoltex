import pygame, sys
from game import button, states, utils



def play_menu(screen):
    pygame.display.set_caption("Play")
    play_background = pygame.image.load("assets/play_background.jpg")
    play_background = pygame.transform.scale(play_background, screen.get_size()).convert()

    while True:
        screen.blit(play_background, (0, 0))
        play_mouse_pos = pygame.mouse.get_pos()

        play_text = utils.get_font(150).render("Play", True, "#b68f40")
        play_text_rect = play_text.get_rect(center=(640, 100))

        back_button = button.Button(image=None, pos=(640, 400), 
                             text_input="Back", font=utils.get_font(75), 
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