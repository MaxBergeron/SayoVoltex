import pygame, sys
from game import button, states, utils


def options_menu(screen):
    pygame.display.set_caption("Menu")
    options_background = pygame.image.load("assets/options_background.png")
    options_background = pygame.transform.scale(options_background, screen.get_size()).convert()
    while True:
        
        screen.blit(options_background, (0, 0))

        options_mouse_pos = pygame.mouse.get_pos()

        options_text = utils.get_font(150).render("OPTIONS MENU", True, "#b68f40")
        options_text_rect = options_text.get_rect(center=(640, 100))

        set_keybinds_button = button.Button(image=None, pos=(640, 250), 
                             text_input="SET KEYBINDS", font=utils.get_font(75), 
                             base_color="#d7fcd4", hovering_color="White")
        
        back_button = button.Button(image=None, pos=(640, 400), 
                             text_input="Back", font=utils.get_font(75), 
                             base_color="#d7fcd4", hovering_color="White")

        screen.blit(options_text, options_text_rect)

        for b in [set_keybinds_button, back_button]:
            b.change_color(options_mouse_pos)
            b.update(screen)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if set_keybinds_button.check_for_input(options_mouse_pos):
                    print("Set Keys button clicked!")
                    return states.SET_KEYBINDS
                elif back_button.check_for_input(options_mouse_pos):
                    return states.MENU
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return states.MENU

        pygame.display.flip()

                    


